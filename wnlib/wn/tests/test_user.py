import unittest, sys
sys.path.append('controllers')
sys.path.append('lib')

import wn, wn.model, wn.install
import wn.backends

class TestUsers(unittest.TestCase):
	def setUp(self):
		import conf
		conf.db_name = 'test1'
		wn.install.setup_db()
		wn.install.setup_doctypes()

	def test_create(self):
		"""test create user"""
		user= wn.model.new([{'doctype':'User', 'first_name':'Test', 'email':'test@erpnext.com'}])
		user.insert()
		user.set_password('test1')
	
	def tearDown(self):
		wn.install.remove()
		wn.request, wn.response = None, None	

if __name__=='__main__':
	unittest.main()