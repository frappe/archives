# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

attachments_folder = "tree_species"

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
	
	def validate(self):
		self.doc.page_name = self.doc.name.lower().replace(" ", "-")
		if self.doc.fields.get("__islocal"):
			self.doc.publish = 1
			
	def get_context(self):
		self.local_names = ", ".join([l.local_name for l in \
			self.doclist.get({"doctype": "Tree Species Local Name"})])