"""
Role based permissions based on `role permissions`
"""

import wn, wn.backends

def allowed(doctype, perm_type, user=None):
	"""return true if `user` (or current user) is allowed access of type perm_type"""
	if not doctype:
		raise Exception, "doctype must not be %s" % doctype
	
	if not user and wn.response:
		user = wn.response.session.get('user')

	if not user:
		raise Exception, "user must not be %s" % user
		
	if doctype=='DocType' and perm_type=='read':
		return True # should be allowed to read!
				
	return wn.backends.get('mysql').sql("""select count(*) 
		from user_role, role_permission where
		user_role.user = %s
		and user_role.role = role_permission.role
		and role_permission.for_doctype = %s
		and role_permission.`%s` = 1""" % ('%s', '%s', perm_type), (user, doctype), as_list=1)[0][0]
		
def get_all(user=None):
	"""return all permissions for the user in dict format"""
	if not user and wn.response:
		user = wn.response.session.get('user')

	rplist = wn.backends.get('mysql').sql("""select distinct r.for_doctype, r.read, r.write, r.create
		from user_role, role_permission r
		where user_role.user = %s
		and user_role.role = r.role""", user)
		
	out = {}
	for rp in rplist:
		for p in 'read', 'write', 'create':
			if rp[p]:
				out.setdefault(rp['for_doctype'], {})[p] = rp[p]
				
	return out