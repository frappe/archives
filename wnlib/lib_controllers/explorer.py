import wn, wn.app, wn.model

@wn.app.whitelist()
def get_doctype_list():
	"""get list of doctypes with read permission"""
	wn.mysql.sql("""select t1.doctype from role_permission t1, user_role t2
		where t2.user=%s
		and t2.role = t1.role
		and t1.read = 1""")
	wn.response.write()