# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes, requests
from webnotes.utils.file_manager import save_file

@webnotes.whitelist(allow_guest=True)
def get_trees(north, south, east, west):
	return webnotes.conn.sql("""select tree_species, local_name, latitude, longitude, address_display, creation 
		from tabTree where latitude between %s and %s
		and longitude between %s and %s""", 
		(south, north, west, east), as_dict=True)

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
		
	def validate(self):
		import base64, shutil
		
		for img_name in ("tree_image", "leaf_image"):
			if self.doc.fields.get(img_name) and len( self.doc.fields.get(img_name)) > 100:
				setattr(self, img_name, base64.b64decode(self.doc.fields.get(img_name)))
				self.doc.fields[img_name] = None
				
		self.set_address()
				
	def on_update(self):
		if getattr(self, "tree_image", None):
			webnotes.conn.set_in_doc(self.doc, "tree_image", save_file(self.doc.name + "-tree.jpg", 
				self.tree_image, self.doc.doctype, self.doc.name).file_name)

		if getattr(self, "leaf_image", None):
			webnotes.conn.set_in_doc(self.doc, "leaf_image", save_file(self.doc.name + "-leaf.jpg", 
				 self.leaf_image, self.doc.doctype, self.doc.name).file_name)
				 
	def set_address(self):
		if not self.doc.country:
			response = requests.get("http://nominatim.openstreetmap.org/reverse", params = {
				"format": "json",
				"lat": self.doc.latitude,
				"lon": self.doc.longitude,
				"address_details": 1,
				"zoom": 18
			})
			response_json = response.json()
			if response_json:
				self.doc.address_display = response_json["display_name"]
				for key in response_json["address"]:
					if self.bean.meta.get_field(key):
						self.doc.fields[key] = response_json["address"][key]
