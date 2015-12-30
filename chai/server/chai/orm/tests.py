import unittest
from chai.orm.meta import Meta

class MetaTest(unittest.TestCase):
	"""
	Metamodel test. Will test creation and modification of the the projects.project
	table
	"""
	def setUp(self):
		"""
		chai.connect should connect to default database
		"""
		chai.connect()
		
	def test_creation(self):
		"""
		testing creation of new table
		"""
		self.meta = Meta('projects.project')
		self.meta.sync()

	def test_table_created(self):
		"""
		testing if table was created
		"""
		self.assertTrue(chai.database.has_table('project'))

	def test_columns_name(self):
		"""
		testing if columns are created
		"""
		self.assertTrue(self.meta.has_column('project_name'))
		
	def test_column_type(self):
		"""
		test if right type of column was created
		"""
		self.assertTrue(self.meta.get_col_type('project_name')==('Data', '180'))
		
	def test_add_column(self):
		"""
		test if column was added
		"""
		self.meta.attributes.append(Model({'type':'Currency', 'name':'budget'}))
		self.meta.sync()

		self.assertTrue(self.meta.has_column('budget'))
		self.assertTrue(self.meta.get_col_type('budget')==('Currency'))		
	
	def tearDown(self):
		"""
		Delete the created table
		"""
		chai.database.drop_table('project')
		
if __name__=='__main__':
	unittest.main()
	