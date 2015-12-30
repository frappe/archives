# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license
# Authors: Rushabh Mehta (@rushabh_mehta)


class Table():
	"""
	Wrapper around a database table
	"""
	db_columns = {}
	meta_columns = {}
	
	def __init__(self):
		pass
	
	def get_columns_from_attributes(self):
		"""
		Load columns from attributes
		"""
	
	def get_columns_from_database(self):
		"""
		Load columns from database
		"""
		sql = chai.database.execute

		self.show_columns = sql("desc `%s`" % self.name)
		for c in self.show_columns:
			self.db_columns[c[0]] = {'name': c[0], 'type':c[1], 'index':c[3], 'default':c[4]}
				
	def exists(self):
		"""
		Returs true if table exists
		"""
		return self.table_name in chai.database.get_all_tables()

	def build_col_ddl(self, col):
		"""
		Returns column definition in DDL
		"""
		return '%s %s '

	def get_cols(self):
		"""
		Returns column definitions
		"""
	
	def has_column(self):
	
	def create(self):
		"""
		Create table based on attributes
		"""
		sql = chai.database.execute
	
		sql("""
		create table `%s`
		(%s)
		engine=%s
		""" % (self.model.model_name, self.get_cols(), self.model.engine or 'InnoDB'))
	
	def alter(self):
		"""
		Sync columns and attributes
		"""
		self.add_missing_columns()
		self.delete_extra_columns()

		self.add_missing_index()
		self.delete_extra_index()
			
	def sync(self):
		"""
		Create / alter the table based on attributes
		"""
		
		if self.exists():
			self.alter()
		else:
			self.create()
			