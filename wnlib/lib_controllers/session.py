import wn, wn.model

class Session(wn.model.DocList):
	def before_insert(self):
		"""create sid and boot"""
		self.set('name', wn.random_sha1())
		self.set('user', wn.request.params['user'])
		self.boot()
	
	def boot(self):
		"""boot non-guest user with roles and defaults"""
		import json
		user = wn.model.get('User', wn.request.params['user'])
		self.boot = {
			'profile': {
				'name': user.get('name'),
				'first_name': user.get('first_name'),
				'last_name': user.get('last_name'),
				'roles': user.get_roles(),
				'permissions': user.get_permissions()
			}
		}
		self.set('boot', json.dumps(self.boot, default=wn.json_type_handler))
		
	def resume(self):
		"""resume session"""
		import json
		self.boot = json.loads(self.get('boot'))
	