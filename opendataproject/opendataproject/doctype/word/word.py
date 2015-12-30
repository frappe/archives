# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
		
	def get_context(self):
		self.doc.data_sets = webnotes.conn.sql("""select ds.name, ds.title, ds.row_count 
				from `tabWord Data Set` wds, `tabData Set` ds
				where wds.word=%s and wds.data_set = ds.name
				order by ds.title desc""", self.doc.name, as_dict=True)