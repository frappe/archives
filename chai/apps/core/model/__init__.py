import chai.orm.model

class Model(chai.orm.model.Model):
	def __init__(self):
		pass
		
	def sync(self):
		"""
		Create/alter the database table
		"""
		from chai.orm.table import Table
		self.table = Table(self.attributes)
		self.table.sync()