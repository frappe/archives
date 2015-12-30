# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license

class Base():
	"""
	Base class of all models. Contains methods for persistence
	"""	
	def __init__(self, attributes=None):
		self.attributes = attributes or {}
		
	def save(self):
		"""
		Save the model
		"""
		pass
		
	def sync(self):
		"""
		Sync the model with database schema
		"""
		pass