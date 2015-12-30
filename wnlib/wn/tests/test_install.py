import unittest, sys
sys.path.append('controllers')
sys.path.append('lib')

import wn, wn.model, wn.app
import wn.backends
import conf
import json

class TestInstall(unittest.TestCase):
	def setUp(self):
		import wn.install
		wn.test_sid = None
		conf.db_name = 'test1'
		wn.install.setup_db()
		wn.install.setup_doctypes()
		
	def test_login_and_startup(self):
		wn.model.new([{"doctype":"User", "email":"test@erpnext.com", "first_name":"Test"}]).insert()
		wn.model.get('User', 'test@erpnext.com').set_password('test1')
			
		self.assertEquals(wn.app.request("wn.app.login", {"user": "test@erpnext.com",
			"password":"test1"}, method='POST'), {"info":["Logged In"]})
		
		startup = wn.app.request("wn.app.startup", {})
		self.assertTrue(startup.get('boot'))
		self.assertEquals(startup.get('boot').get('profile').get('name'), 
			'test@erpnext.com')
		
	def tearDown(self):
		import wn.install
		wn.backends.close()
		wn.install.remove()
		
if __name__=='__main__':
	unittest.main()