import webnotes

def get_context():
	out = []
	added = []
	for t in webnotes.conn.sql("""select distinct local_name, parent as value from 
		`tabTree Species Local Name` where ifnull(local_name,'')!='' 
		order by local_name asc""", as_dict=1):
		if not t.local_name in added:
			t.tokens = t.local_name.split() + t.value.split()
			out.append(t)
			added.append(t.local_name)

	return {
		"tree_species": out
	}