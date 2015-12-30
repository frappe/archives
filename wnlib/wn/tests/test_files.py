import unittest, sys

sys.path.append('controllers')
sys.path.append('lib')

import os
import wn, wn.model
import wn.backends

import conf

class TestFiles(unittest.TestCase):
	def setUp(self):
		self.conn = wn.backends.get('files')
		
	def test_insert(self):
		self.conn.insert_doclist([{"doctype":"DocType", "name":"Test", "testkey":"testval"},
		{"doctype":"DocField", "fieldtype":"Data", "fieldname":"test_data", "reqd":1},
		{"doctype":"DocField", "fieldtype":"Date", "fieldname":"test_date"},
		{"doctype":"DocField", "fieldtype":"Text", "fieldname":"test_text"},
		{"doctype":"DocField", "fieldtype":"Int", "fieldname":"test_int"},
		{"doctype":"DocField", "fieldtype":"Float", "fieldname":"test_float"},
		{"doctype":"DocField", "fieldtype":"Currency", "fieldname":"test_currency"},
		])
		
		self.assertTrue(os.path.exists('models/doctype/test.json'))
	
	def test_get(self):
		self.test_insert()
		doclist = self.conn.get('DocType', "Test")
		self.assertTrue('test_data' in [t.get('fieldname') for t in doclist])
	
	def test_get_value(self):
		self.test_insert()
		self.assertTrue(self.conn.get_value('DocType', 'Test', 'testkey')=='testval')
	
	def tearDown(self):
		self.conn.remove("DocType", "Test")
		
		
		
if __name__=='__main__':
	unittest.main()