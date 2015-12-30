"""
Stores all objects in a single table `_statement (name, key, value)`
"""

from wn.backends.mysql import MySQLBackend

class MySQLObjectBackend(MySQLBackend):
	backend_type = 'mysql_obj'
	def get(self, name, name1=None):
		"""get object by name"""
		
		# standard caller is doctype, name
		# but since doctype is irrelevant,
		# call by name (also give user to ignore the name)
		if name1: name = name1
		
		obj = {}
		for (key, value) in self.sql("""select `key`, `value` from `_statement` where name=%s""", 
			name, as_list=1):
			if key in obj:
				# vector
				if not isinstance(obj[key], list):
					obj[key] = [obj[key],]
				obj[key].append(value)
			else:
				obj[key] = value
		
		return obj
		
	def insert(self, obj):
		"""insert object, give name if reqd"""
		if not obj.get('name'):
			obj['name'] = wn.random_sha1()
			
		self.update(obj)
	
	def insert_statement(self, name, key, val):
		"""insert single statement"""
		self.sql("""insert into _statement(`name`, `key`, `value`) values 
			(%s, %s, %s)""", (name, key, val))
	
	def update(self, obj):
		"""remove and rewrite the object"""
		self.remove(obj.get('name'))
		for key in obj:
			val = obj[key]
			if isinstance(val, list):
				for v in val:
					self.insert_statement(obj['name'], key, v)
			else:
				self.insert_statement(obj['name'], key, val)

	def exists(self, doctype, name):
		"""return true if record exists"""
		return self.sql("""select count(*) from `_statement` 
			where `name`=%s""", name) and True or False
	
	def remove(self, name):
		"""remove object by name"""
		self.sql("""delete from _statement where name=%s""", name)
		
	def get_value(self, doctype, name, key):
		values = self.sql("""select value from _statement 
			where name=%s and`key`=%s""", (name, key))
		
		if len(values) > 1: 
			return [r['value'] for r in values]
		elif len(values)==1:
			return r['value']
		else:
			return None
			
	def setup(self, doclist):
		pass
		
	