"""
User Controller
---------------
A MySQL user is created for each user and permissions are delegated to MySQL
"""

import wn.model, wn.permissions
from wn.translate import _

class User(wn.model.DocList):
	def autoname(self):
		"""name is email if not given"""
		if not self.get('name'):
			self.set('name', self.get('email'))
	
	def set_password(self, password):
		"""set encrypted password"""
		self.backend.sql("""update `user` set `password`=password(%s) where name=%s""", 
			(password, self.get('name')))
	
	def authenticate(self, password):
		"""validate password"""
		if not self.backend.sql("""select name from user where name=%s 
			and `password`=password(%s)""", 
			(self.get('name'), password)):
			raise Exception, _("Incorrect Login")
			
	def get_roles(self):
		"""return list of roles"""
		return [r['role'] for r in self.backend.sql("""select role from user_role where user=%s""", 
			self.get('name'))]
	
	def get_permissions(self):
		"""return dict of permissions"""
		wn.permissions.get_all(self.get('name'))