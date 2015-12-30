import webnotes

def get_context():
	return {
		"doctype": "Data Set",
		"name": webnotes.form_dict.name,
		"comment_list": webnotes.conn.sql("""\
			select comment, comment_by_fullname, creation
			from `tabComment` where comment_doctype="Data Set"
			and comment_docname=%s order by creation""", webnotes.form_dict.name, as_dict=1)
	}
	