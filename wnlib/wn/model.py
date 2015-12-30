import wn, wn.backends, wn.app

class DocList():	
	def __init__(self, doclist=None, name=None):
		self.doclist = []
		self._backend = None
		
		if isinstance(doclist, dict):
			self.set_doclist([doclist])
		
		elif isinstance(doclist, list):
			self.set_doclist(doclist)
			
		elif name and isinstance(doclist, basestring):
			self.load(doclist, name)
	
	def set_doclist(self, doclist):
		"""set `doc` and `doclist` properties"""
		self.doclist = doclist
		self.doc = doclist[0]
	
	def load(self, doctype, name):
		"""load from backend"""
		self.backend = wn.backends.get_for(doctype)
		doclist = self.backend.get(doctype, name)
		if not doclist:
			raise wn.NotFoundError, "%s, %s" % (doctype, name)
			
		self.set_doclist(doclist)
		
	def get(self, name, default=None):
		"""get a value from the main doc, or a list of child docs based on filters"""
		if isinstance(name, basestring):
			return self.doc.get(name, default)
		
		elif isinstance(name, dict):
			return filter(lambda d: False not in map(lambda key: d.get(key)==name[key], name.keys()), 
				self.doclist) or default
		else:
			raise Exception, 'unable to identify %s' % str(name)
	
	def set(self, name, value):
		"""set local value in main doc"""
		self.doc[name] = value
	
	@property
	def backend(self):
		"""get backend"""
		if not self._backend:
			self._backend = wn.backends.get_for(self.get('doctype'))
		return self._backend
	
	def insert(self):
		"""insert the doclist"""
		self.trigger('autoname')
		self.trigger('before_insert')
		self.backend.insert_doclist(self.doclist)
		self.trigger('after_insert')

	def update(self):
		"""update the doclist"""
		self.trigger('before_update')
		self.backend.update_doclist(self.doclist)
		self.trigger('after_update')
	
	def trigger(self, method):
		hasattr(self, method) and getattr(self, method)()

def if_allowed(perm='read'):
	"""decorator that throws a `wn.PermissionError` if the first argument
	   is not allowed"""
	
	# TODO: a better way to validate whether
	# request is remote (or not)
	def get_function(fn):
		def wrapper(*args, **kw):
			import wn.permissions
			if wn.check_permissions:
				doctype = args and args[0] or kw['doctype']
				if wn.permissions.allowed(doctype, perm):
					return fn(*args, **kw)
				else:
					raise wn.PermissionError, 'no permission for "%s"' % doctype
			else:
				return fn(*args, **kw)

		return wrapper
	
	return get_function

@wn.app.whitelist()
def get(doctype, name):
	"""get a doclist object of the give doctype, name"""
	if isinstance(doctype, basestring):
		o =  _get_doctype_object(doctype)(doctype, name)
	elif isinstance(doctype, list):
		o = _get_doctype_object(doctype[0].get('doctype'))(doctype)
	else:
		raise Exception, "must pass doctype as string or doclist"

	return _object_or_raw(doctype, name, o)
	
def _object_or_raw(doctype, name, o):
	"""send raw if called from request"""
	if wn.check_permissions and wn.request.params['_method']=='wn.model.get'\
		and wn.request.params['doctype']==doctype and wn.request.params['name']==name:
		return o.doclist
	else:
		return o

@if_allowed()
def _get_doctype_object(doctype):
	"""make a object of the class of the controller of the given doctype"""
	return _import_object(_get_controller_name(doctype))

def _import_object(txt):
	"""import a reference from a python module"""
	m = txt.split('.')	
	module = __import__('.'.join(m[:-1]), fromlist=True)
	return getattr(module, m[-1])

def _get_controller_name(doctype):
	"""get controller module string for the doctype"""
	return wn.model.get_value('DocType', doctype, 'controller', 'wn.model.DocList')

@if_allowed()
def get_value(doctype, name, key, default=None):
	"""get a value"""
	return wn.backends.get_for(doctype).get_value(doctype, name, key, default)

@if_allowed('create')
def new(doctype):
	"""create a new instance of a doctype (pass name or doclist or maindoc)"""
	if isinstance(doctype, dict):
		newobj = _get_doctype_object(doctype.get('doctype'))()
		doclist = [doctype]
	elif isinstance(doctype, list):
		newobj = _get_doctype_object(doctype[0].get('doctype'))()
		doclist = doctype
	else:
		newobj = _get_doctype_object(doctype)()
		doclist = [{"doctype":doctype}]
		
	newobj.set_doclist(doclist)
	return newobj

@wn.app.whitelist()
@if_allowed()
def get_list(**kw):
	"""return list of doctype objects (with listable properties)"""
	return wn.backends.get_for(kw['doctype']).get_list(**kw)
	
@if_allowed()
def exists(doctype, name):
	"""returns true if exists"""
	return wn.backends.get_for(doctype).exists(doctype, name)

def passes(filters, doc):
	"""returns true doc passes fitlers. Filters can be dict or list of lists with
	[key, condition, value]"""
	if not filters: return True
	if isinstance(filters, dict):
		return False not in map(lambda key: doc.get(key)==filters[key], filters.keys())
	else:
		for f in filters:
			v = doc.get(f[0])
			if not eval('v %s f[2]' % (f[1]=='=' and '==' or f[1])):
				return False
		return True