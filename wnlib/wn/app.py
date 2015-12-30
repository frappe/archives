user = None

from webob import Request, Response
import wsgiref.handlers
import wn, wn.model
import json

def application(environ, start_response):
	"""wsgi application method"""
	wn.request = Request(environ)
	wn.response = AppResponse()
	try:
		wn.response.prepare()
		wn.response.process()
		wn.response.cleanup()
	except Exception, e:
		wn.response.body = wn.traceback()

	return wn.response(environ, start_response)

class AppResponse(Response):
	"""	AppResponse executes the request:
		- loads the session (or guest)
		- gets execution method `_method` from request
		- checks if whitelisted
		- starts transaction if post
		- passes control to `_method`
		- commits
		"""
	def __init__(self):
		self.json = {}
		self.sid = None
		self.messages, self.errors, self.logs, self.info = [], [], [], []
		Response.__init__(self)
	
	def error(self, txt): self.errors.append(txt)
	def message(self, txt): self.messages.append(txt)
	def log(self, txt): self.logs.append(txt)
	def write(self, txt): self.info.append(txt)

	def prepare(self):
		"""load session from cookie or parameter"""
		wn.check_permissions = False 
		self.sid = wn.request.cookies.get('sid') or wn.request.params.get('sid') or 'guest'
		
		def new_session():
			self.session = wn.model.new([{"doctype":"_session", "user":"Guest"}])
			self.sid = 'guest'
		
		if self.sid:
			try:
				self.session = wn.model.get("_session", self.sid)
				self.session.resume()
			except wn.NotFoundError:
				new_session()
		else:
			new_session()

	def get_method(self):
		"""get execution method"""
		# check for "_method"
		if not '_method' in wn.request.params:
			self.error('no method')
			return
		
		# import module
		m = wn.request.params['_method'].split('.')
		module_name = '.'.join(m[:-1])
		try:
			module = __import__(module_name, fromlist=True)
		except Exception,e:
			self.error('unable to import %s' % module_name)
			return
		
		# get method
		method = getattr(module, m[-1], None)
		if not method:
			self.error('no method %s' % m[-1])
			return
		
		# check if its whitelisted
		if not method in whitelisted:
			self.error('method not allowed')
			return
		
		if self.sid=='guest' and method not in guest_whitelisted:
			self.error('method not allowed for guest')
			return

		return method
			
	def process(self):
		"""process the response, call the specified method"""
		method = self.get_method()
		conn = wn.backends.get('mysql')
		if method:
			# execute
			try:
				params = dict(wn.request.params)
				del params['_method']
				wn.check_permissions = True

				wn.request.method=='POST' and conn.begin()
				ret = method(**params)
				if ret: self.write(ret)
				wn.request.method=='POST' and conn.commit()
			except wn.PermissionError, e:
				wn.request.method=='POST' and conn.rollback()
				wn.response.error(str(e))
			except Exception, e:
				wn.request.method=='POST' and conn.rollback()
				wn.response.error(wn.traceback())

	def cleanup(self):
		"""make response body"""
		if self.messages:
			self.json['messages'] = self.messages
		if self.errors:
			self.json['errors'] = self.errors
		if self.logs:
			self.json['logs'] = self.logs
		if self.info:
			self.json['info'] = self.info
		if self.json:
			self.body = json.dumps(self.json, default=wn.json_type_handler)


whitelisted = []
guest_whitelisted = []
def whitelist(allow_guest=False, allow_roles=[]):
	"""
	decorator for whitelisting a function @wn.app.whitelist()
	
	Note: if the function is allowed to be accessed by a guest user,
	it must explicitly be marked as allow_guest=True
	
	for specific roles, set allow_roles = ['Administrator'] etc.
	"""
	def get_function(fn):
		global whitelisted, guest_whitelisted
		whitelisted.append(fn)

		if allow_guest:
			guest_whitelisted.append(fn)

		if allow_roles:
			if not (set(allow_roles) & set(wn.user.roles())):
				raise PermissionError, "Method not allowed"

		return fn

	return get_function

@whitelist(allow_guest=True)
def login(user, password):
	"""verify login creds and create a session"""
	try:
		# don't check permissions for user and session objects
		wn.check_permissions = False 
		
		wn.model.get('User', user).authenticate(password)
		session = wn.model.new('_session')
		session.insert()
		wn.response.sid = session.get('name')
		wn.response.write('Logged In')
		wn.response.set_cookie('sid', session.get('name'), path='/')
	except wn.NotFoundError, e:
		wn.response.write('No such user')
	except Exception, e:
		wn.response.error(wn.traceback())
		wn.response.write('There were errors')

@whitelist()
def startup():
	"""startup"""
	wn.response.json['boot'] = json.loads(wn.response.session.get('boot'))

@whitelist()
def logout():
	"""clear session"""
	if getattr(wn, 'sid', None):
		wn.model.remove('_session', wn.sid)
		wn.response.write('Logged Out')

test_sid = None # save sid for subsequent queries
def request(_method, params, **args):
	"""test method"""
	global test_sid
	import urllib
	params['_method'] = _method
	if test_sid:
		wn.request = Request.blank('/?'+urllib.urlencode(params), cookies={'sid':test_sid}, **args)
	else:
		wn.request = Request.blank('/?'+urllib.urlencode(params), **args)
		
	wn.response = AppResponse()
	wn.response.prepare()
		
	wn.response.process()
	wn.response.cleanup()
	test_sid = wn.response.sid
	return wn.response.json