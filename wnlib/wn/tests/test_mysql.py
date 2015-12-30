import unittest, sys

sys.path.append('controllers')
sys.path.append('lib')

import wn
import wn.backends, wn.install
import conf

class TestMySQL(unittest.TestCase):
	def setUp(self):
		conf.db_name = 'test1'
		wn.install.setup_db()
		self.conn = wn.backends.get('mysql')

	def tearDown(self):
		self.conn.close()
		wn.install.remove()
	
	def test_setup(self):
		from wn.model import DocList
		table_def = DocList([{"doctype":"DocType", "name":"Test"},
		{"doctype":"DocField", "fieldtype":"Data", "fieldname":"test_data", "reqd":1},
		{"doctype":"DocField", "fieldtype":"Date", "fieldname":"test_date"},
		{"doctype":"DocField", "fieldtype":"Text", "fieldname":"test_text"},
		{"doctype":"DocField", "fieldtype":"Int", "fieldname":"test_int"},
		{"doctype":"DocField", "fieldtype":"Float", "fieldname":"test_float"},
		{"doctype":"DocField", "fieldtype":"Currency", "fieldname":"test_currency"},
		])
		self.conn.setup(table_def)
		self.assertTrue("test" in self.conn.get_tables())
	
	def test_insert(self):
		self.test_setup()
		rec = {"doctype":"Test", "name":"r1", "test_data":"hello"}
		self.conn.insert(rec)
		self.assertEquals(self.conn.get("Test", "r1")[0].get("test_data"), rec.get("test_data"))
	
	def test_mandatory(self):
		self.test_setup()
		rec = {"doctype":"Test", "name":"r1"}
		self.assertRaises(wn.ValidationError, self.conn.insert, rec)
	
	def test_update(self):
		self.test_insert()
		rec = {"doctype":"Test", "name":"r1", "test_data":"hello sir"}
		self.conn.update(rec)
		self.assertEquals(self.conn.get("Test", "r1")[0].get("test_data"), rec.get("test_data"))
	

if __name__=='__main__':
	unittest.main()