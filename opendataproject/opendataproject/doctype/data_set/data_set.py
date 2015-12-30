# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
		
	def get_context(self):
		from data.utils import get_file_data
		from webnotes.utils import get_path
		headers, self.doc.data = get_file_data(get_path("app", "downloads", 
			"data.gov.in", self.doc.raw_filename))
		self.doc.max_cols = max([len(r) for r in self.doc.data])
		
		self.doc.comment_list = webnotes.conn.sql("""\
			select comment, comment_by_fullname, creation
			from `tabComment` where comment_doctype="Data Set"
			and comment_docname=%s order by creation""", self.doc.name, as_dict=1)


@webnotes.whitelist(allow_guest=True)
def public_save(name, legend, head_row, selected_rows, first_column, last_column, chart_type, transpose):	
	ds = webnotes.bean("Data Set", webnotes.form_dict.name)
	ds.ignore_permissions = True
	ds.doc.head_row = head_row
	ds.doc.legend = legend
	ds.doc.selected_rows = selected_rows
	ds.doc.first_column = first_column
	ds.doc.last_column = last_column
	ds.doc.chart_type = chart_type
	ds.doc.transpose = cint(transpose)
	ds.save()

@webnotes.whitelist(allow_guest=True)
def get_settings(name):
	return webnotes.conn.sql("""select legend, rating,
		head_row, selected_rows, first_column, last_column, chart_type, transpose
		from `tabData Set` where name=%s""", name, as_dict=True)[0]

@webnotes.whitelist(allow_guest=True)
def set_rating(name, rating):
	d = webnotes.conn.sql("""select ifnull(rating, 0) as rating, 
		ifnull(ratings_polled, 0) as ratings_polled
		from `tabData Set` where name=%s""", name, as_dict=1)[0]
	
	new_rating = ((d.rating * d.ratings_polled) + cint(rating)) / (d.ratings_polled + 1)
	webnotes.conn.set_value("Data Set", name, "rating", new_rating)
	webnotes.conn.set_value("Data Set", name, "ratings_polled", d.ratings_polled + 1)
	
	return new_rating