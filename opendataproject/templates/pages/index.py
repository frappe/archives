import webnotes

def get_context():
	return {
		"data_sets": webnotes.conn.sql("""select name as id, title, raw_filename, 
			row_count, rating, url, description
			from `tabData Set` 
			where ifnull(title, '')!=''
			order by rating desc, name asc""", as_dict=True)
	}