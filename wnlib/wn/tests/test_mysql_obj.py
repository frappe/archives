import unittest, sys

sys.path.append('controllers')
sys.path.append('lib')

import wn, wn.model, wn.install
import conf


class TestMySQLObj(unittest.TestCase):
	def setUp(self):
		conf.db_name = 'test1'
		wn.install.setup_db()
		wn.model.get('DocType', '_statement').setup()
		self.conn = wn.backends.get('mysql_obj')

	def tearDown(self):
		self.conn.sql("drop database test1")
		self.conn.close()
		
	def test_insert(self):
		rec = {"doctype":"Test", "name":"r1", "test_data":"hello"}
		self.conn.insert(rec)
 		#print self.conn.sql("""select * from _statement""")
		self.assertEquals(self.conn.get("Test", "r1").get("test_data"), rec.get("test_data"))		
		
if __name__=='__main__':
	unittest.main()
