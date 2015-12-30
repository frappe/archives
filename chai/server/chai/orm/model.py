# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license
# Authors: Rushabh Mehta (@rushabh_mehta)

class Model:
	"""
	Wrapper around a model object / a database record
	"""
	def __init__(self, model=None, id=None, attributes=None):
		"""
		Load the model from database if id is given
		"""
		self.model = model
		self.id = id
		self._backend = None
		
		if attributes:
			self.load(attributes)
		
		if model and id:
			self.load_from_db()

			
	def load(self, attributes):
		"""
		Load model attributes as given
		"""
		self.__dict__.update(attributes)

		
	def load_from_db(self):
		"""
		Load model attributes from db
		"""
		self._source = 'database'

	
	def __getter__(self, name):
		"""
		Getter does not throw exception
		"""
		return self.__dict__.get(name, None)
		
	def save(self):
		"""
		Insert / Update the model
		"""
		if self._backend == 'database':
			self.insert_or_update()
			
		else:
			self.write_to_file()
	
	def insert_or_update(self):
		"""
		Insert or update db record
		"""
			
	def write_to_file(self):
		pass