class Collection:
	"""
	A collection is a ordered list of models,
	Can be loaded from a file or db
	"""
	def __init__(self, model=None, id=None, models=None):
		self.models = models

		# parent and child pattern
		self.model = model
		self.id = id
			
		elif model and id:
			self.load_model_set()
		
	def load_from_file(self):
		"""
		Load model from file. The id contains the path
		"""
		import os, chai
		from chai.orm.model import Model

		model_name = self.model_id.split('.')[-1]
		
		f = open(os.path.join(chai.app_path, model.replace('.', os.path.sep), model_name + '.model', 'r')
		
		ml = eval(r.read())
		f.close()
		ml = self.process_models(ml)
		self.render_models(ml)
		
	def process_models(self, ml):
		"""
		Returns scrubbed model list
		"""
		return ml
	
	def render_models(self, ml):
		"""
		Create model objects
		"""
		self.models = [Model(attributes=m) for m in ml]
		
	def get_collection(self, f):
		"""
		Returns collection by filter
		"""
		ret = []
		for m in self.models:
			is_subset = True
			for k in f:
				if m.__dict__.get(k,None)!=f[k]:
					is_subset = False
					break
		
			if is_subset:
				ret.append(m)

			
		return Collection(models=ret)
		
	def get(self, id):
		"""
		Get by id
		"""
		for m in self.models:
			if m.id==id: return m
	
	def load_model_set(self):
		"""
		Loads a collection of the model specified and its child records
		as specified in its meta
		"""
		
class MetaCollection(Collection):
	"""
	Meta collection is a collection of a meta model
	"""
	def __init__(self, model_id):
		self.load_from_file(model_id)
		
	def process_model(self, ml):
		"""
		Removes 'template' models that are templates and updates attributes from templates
		"""
		template = None
		for i in range(len(ml)):
			m = ml[i]
			if not m.get('is_template'):
				template = m
				del ml[i]

			elif template:
				m = template.update(m)

		return ml