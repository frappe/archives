# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
		
	def get_context(self):
		if self.doc.region_type=="State":
			self.doc.districts = webnotes.conn.sql_list("""select name from tabRegion 
				where parent_region = %s
				order by name asc""", self.doc.name)