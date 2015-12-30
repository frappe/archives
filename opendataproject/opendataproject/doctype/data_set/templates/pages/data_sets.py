import webnotes

def get_context():
	data_sets = webnotes.conn.sql("""select name, title, description from `tabData Set` 
			order by title asc""", as_dict=True)
	return {
		"data_sets": data_sets
	}