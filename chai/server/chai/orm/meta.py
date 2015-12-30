# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license
# Authors: Rushabh Mehta (@rushabh_mehta)

from chai.orm.collection import MetaCollection

class Meta(Table):
	"""
	Represents a meta model (DocType in old style)
	"""
	def __init__(self, model_id):
		self.model_id = model_id
		self.load()

	def load(self):
		"""
		Load from files
		"""
		self.all = MetaCollection('core.model', model_id)

		self.model = self.all.get(self.model_id)
		self.attributes = self.all.get_collection({'model':'model_attribute'})
		self.permissions = self.all.get_collection({'model':'model_permission'})