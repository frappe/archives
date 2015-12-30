# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license
# Authors: Rushabh Mehta (@rushabh_mehta)

class Database:
	"""
	Database wrapper
	"""
	def __init__(self, apps=[]):
		self.apps = ['core'] + apps
		
	def sync(self):
		"""
		Updates the schema of all the application models
		"""
		all_models = chai.models.get_all_models(self.apps)
		map(self.sync_model, all_models)
		
	def sync_model(self, model):
		"""
		Create / Update database table to reflect model and model attributes
		"""
		import sqlalchemy
		
	def get_all_tables(self):
		"""
		Returns all tables
		"""