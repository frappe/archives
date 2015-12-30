"""
Backends must

Methods:

get
insert
update
remove

optionally sql
"""

connections = {}

def get(backend_type, **args):
	backend_type = backend_type.lower()

	if 'user' in args:
		backend_type = backend_type + ':' + args['user']
	
	args['name'] = backend_type
			
	global connections
	if not connections.get(backend_type):
		if backend_type=='mysql_obj':
			import mysql_obj
			connections[backend_type] = mysql_obj.MySQLObjectBackend(**args)

		elif backend_type.startswith('mysql'):
			import mysql
			connections[backend_type] = mysql.MySQLBackend(**args)
		
		elif backend_type.lower()=='files':
			import files
			connections['files'] = files.FilesBackend()

	return connections[backend_type]

@property
def mysql():
	return get('mysql')

def get_for(doctype):
	if doctype=='DocType':
		return get('files')
	else:
		return get('mysql')

def close():
	clist = connections.values()
	for conn in clist:
		conn.close()
