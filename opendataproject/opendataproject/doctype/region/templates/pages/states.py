import webnotes

def get_context():
	return {
		"states": webnotes.conn.sql_list("""select name from tabRegion where region_type='State'
			order by name asc""")
	}