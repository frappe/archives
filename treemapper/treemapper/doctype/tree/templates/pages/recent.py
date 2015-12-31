import webnotes

@webnotes.whitelist(allow_guest=True)
def get_list(start=0):
	out = webnotes.conn.sql("""select tree_species, address_display, 
		tree_image from `tabTree` order by creation desc limit 20""", as_dict=1)
	return out