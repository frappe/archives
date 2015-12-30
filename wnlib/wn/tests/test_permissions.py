import unittest, sys
sys.path.append('controllers')
sys.path.append('lib')

import wn, wn.model, wn.install, wn.tests, wn.permissions
import wn.backends

class TestPermissions(unittest.TestCase):
	def setUp(self):
		import conf
		conf.db_name = 'test1'
		wn.request, wn.response, wn.check_permissions = None, None, False
		wn.install.setup_db()
		wn.install.setup_doctypes()
		wn.tests.make_test_doctype()

	def make_perms(self):
		user= wn.model.new([{'doctype':'User', 'first_name':'Test', 'email':'test@erpnext.com'}])
		user.insert()
		user.set_password('test1')
		
		wn.model.new([{'doctype':'Role', 'name':'Test'}]).insert()
		wn.model.new([{'doctype':'User Role', 'user':'test@erpnext.com', 
			'role': 'Test'}]).insert()
		wn.model.new([{'doctype':'Role Permission', 'role':'Test', 'for_doctype':'Test', 
			'read':1}]).insert()

	def test_basic(self):
		"""test create user"""
		self.make_perms()
		self.assertTrue(wn.permissions.allowed('Test', 'read', 'test@erpnext.com'))
		self.assertFalse(wn.permissions.allowed('Test', 'write', 'test@erpnext.com'))
		self.assertFalse(wn.permissions.allowed('Test', 'write', 'test1@erpnext.com'))
		
	def test_get_all(self):
		"""test get all permissions"""
		self.make_perms()
		self.assertEquals(wn.permissions.get_all('test@erpnext.com'), {"Test": {"read":1}})
	
	def setup_request(self):
		self.make_perms()
		wn.model.DocList([{"name":"r1", "test_data":"hello", "doctype":"Test"}]).insert()
		
		r = wn.app.request('wn.app.login', {'user':'test@erpnext.com', 
			'password':'test1'}, method='POST')
		self.assertEquals(r, {"info":["Logged In"]})
	
	def test_get(self):
		self.setup_request()
		
		# test model.get
		r = wn.app.request('wn.model.get', {"doctype":"Test", "name":"r1"})
		self.assertEquals(r['info'][0][0].get('test_data'), 'hello')
		
	def test_error_get(self):
		self.setup_request()
		# test permission error (for role)
		r = wn.app.request('wn.model.get', {"doctype":"Role", "name":"Test"})
		self.assertTrue(r.get('errors')[0].startswith('no permission'))
		
	def test_get_list(self):
		self.setup_request()
		r = wn.app.request('wn.model.get_list', {'doctype':'Test'})
		self.assertTrue('r1' in [rec['name'] for rec in r['info'][0]])

	def test_error_get_list(self):
		self.setup_request()
		r = wn.app.request('wn.model.get_list', {'doctype':'Role'})
		self.assertTrue(r.get('errors')[0].startswith('no permission'))


	def tearDown(self):
		wn.backends.close()
		wn.install.remove()
		wn.request, wn.response = None, None
		wn.tests.cleanup_test()

if __name__=='__main__':
	unittest.main()