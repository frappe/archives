import unittest, sys
sys.path.append('controllers')
sys.path.append('lib')

import wn, wn.model, wn.install, wn.tests, wn.app, wn.backends

class TestModels(unittest.TestCase):
	def setUp(self):
		import conf
		conf.db_name = 'test1'
		wn.request, wn.response, wn.check_permissions = None, None, False
		wn.install.setup_db()
		self.files = wn.backends.get('files')
		wn.tests.make_test_doctype()
		self.conn = wn.backends.get('mysql')


	def test_get(self):
		wn.model.DocList([{"name":"r1", "test_data":"hello", "doctype":"Test"}]).insert()
		obj = wn.model.get('Test', 'r1')
		self.assertTrue(obj.test_property)
		self.assertTrue(obj.get('test_data')=='hello')
		
	def test_fail(self):
		self.assertRaises(wn.NotFoundError, wn.model.get, 'Test', 'r2')
		
	def test_duplicate(self):
		wn.model.DocList([{"name":"r1", "test_data":"hello", "doctype":"Test"}]).insert()
		self.assertRaises(Exception, wn.model.DocList([{"name":"r1", "test_data":"hello", 
			"doctype":"Test"}]).insert, None)
	
	def test_exists(self):
		wn.model.DocList([{"name":"r1", "test_data":"hello", "doctype":"Test"}]).insert()
		self.assertTrue(wn.model.exists('Test', 'r1'))
		self.assertFalse(wn.model.exists('Test', 'rx'))
				
	
	def test_update(self):
		doclist = wn.model.DocList([{"name":"r1", "test_data":"hello", "doctype":"Test"}])
		doclist.insert()
		doclist.set('test_data', 'world')
		doclist.update()
		self.assertEquals(wn.model.get_value('Test', 'r1', 'test_data'), 'world')

	def test_list_files(self):
		llist = wn.model.get_list(doctype='DocType')
		self.assertTrue({"name":"User"} in llist)
		self.assertTrue({"name":"Role"} in llist)
		
		llist = wn.model.get_list(doctype='DocType', filters=[["name", "=", "User"]])
		self.assertTrue({"name":"User"} in llist)
		self.assertTrue({"name":"Role"} not in llist)
		
	def test_passes(self):
		d = {'a':5, 'b':6}
		self.assertTrue(wn.model.passes([['a','=',5]], d))
		self.assertFalse(wn.model.passes([['a','<',5]], d))
		self.assertFalse(wn.model.passes([['b','>',10]], d))
		self.assertTrue(wn.model.passes({'a':5}, d))
	
	def test_listable(self):
		listables = wn.model.get('DocType', 'Test').get_listables()
		self.assertTrue('name' in listables)
		self.assertTrue('test_data' in listables)
		self.assertTrue('test_int' in listables)
		self.assertFalse('test_date' in listables)
		self.assertFalse('test_currency' in listables)
	
	def test_list_mysql(self):
		wn.model.DocList([{"name":"r1", "test_data":"hello", "doctype":"Test"}]).insert()
		wn.model.DocList([{"name":"r2", "test_data":"hello1", "doctype":"Test"}]).insert()
		wn.model.DocList([{"name":"r3", "test_data":"hello2", "doctype":"Test"}]).insert()

		llist = wn.model.get_list(doctype='Test')
		self.assertTrue(len(llist)==3)
		self.assertTrue('r1' in [l['name'] for l in llist])
		self.assertTrue('r2' in [l['name'] for l in llist])
		self.assertTrue('r3' in [l['name'] for l in llist])
		self.assertTrue('test_data' in llist[0])
		self.assertFalse('test_currency' in llist[0])

		llist = wn.model.get_list(doctype='Test', filters=[['name','>=', 'r2']])
		self.assertTrue(len(llist)==2)
		self.assertFalse('r1' in [l['name'] for l in llist])
		self.assertTrue('r2' in [l['name'] for l in llist])
		self.assertTrue('r3' in [l['name'] for l in llist])

	def tearDown(self):
		wn.tests.cleanup_test()
		self.conn.close()
		wn.install.remove()
		
if __name__=='__main__':
	unittest.main()
