"""
Files backend

Backend where documents are stored in files.

"""

class FilesBackend:
	cache = {}
	def doc_path(self, doctype, name):
		"""get docpath"""
		import wn, os, conf
		for p in conf.doc_path:
			path = os.path.join(wn.root_path, p, wn.code_style(doctype), wn.code_style(name) + '.json')
			if os.path.exists(path):
				return path
				
		raise wn.NotFoundError, 'Not found ".json" file for %s, %s' % (doctype, name)
				
	def strip_values(self, doclist):
		"""reduce fields before writing in document file"""
		for d in doclist:
			remove_keys = ()
			remove_values = (None, 0)

			key_list = d.keys()
			for key in key_list:
				if key in remove_keys:
					del d[key]
					continue

				if d[key] in remove_values:
					del d[key]
	
	def add_to_cache(self, doclist):
		"""add doclist to cache"""
		self.cache.setdefault(doclist[0]['doctype'], {})[doclist[0]['name']] = doclist
		
	def insert_doclist(self, doclist):
		"""add a new files in the 'models' folder"""
		import json, wn, os
		self.strip_values(doclist)
		
		fpath = os.path.join(wn.root_path, 'models', wn.code_style(doclist[0]['doctype']),
			wn.code_style(doclist[0]['name']) + '.json')
		with open(fpath, 'w') as jsonfile:
			jsonfile.write(json.dumps(doclist, indent=1))
		self.add_to_cache(doclist)
	
	def update_doclist(self, doclist):
		self.insert_doclists(doclist)
		
	def get(self, doctype, name):
		"""get doclist"""
		
		# pick from cache
		if doctype in self.cache and name in self.cache[doctype]:
			return self.cache[doctype][name]
		
		fpath = self.doc_path(doctype, name)
		
		return self.get_doclist_from_file(fpath)
			
	def get_doclist_from_file(self, fpath):
		"""open and read file, parse JSON, return doclist"""
		import json, os
		if os.path.exists(fpath):
			with open(fpath, 'r') as jsonfile:
				try:
					doclist = json.loads(jsonfile.read())
					self.add_to_cache(doclist)
					return doclist
				except Exception, e:
					print "JSON parse error: " + fpath
					raise e
		else:
			return []
			
	def get_list(self, doctype, filters=None, start=None, limit=None):
		"""get multiple doclists"""
		llist = []
		import wn, os, conf
		for p in conf.doc_path:
			for fname in filter(lambda f: f.endswith('json'), 
				os.listdir(os.path.join(wn.root_path, p, doctype))):
					doclist = self.get_doclist_from_file(\
						os.path.join(wn.root_path, p, doctype, fname))
						
					if wn.model.passes(filters, doclist[0]):
						llist.append({"name": doclist[0].get("name")})
		return llist
		
	def get_value(self, doctype, name, key, default=None):
		"""get a particular value"""
		doclist = self.get(doctype, name)
		return doclist and doclist[0].get(key, default) or default
	
	def remove(self, doctype, name):
		import os
		fpath = self.doc_path(doctype, name)
		if os.path.exists(fpath):
			os.remove(fpath)

	def setup(self, doclist):
		pass
		
	def close(self):
		pass