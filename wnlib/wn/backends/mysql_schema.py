"""build and sync schema from doctypes"""

std_columns = ({
	'fieldname': 'name',
	'fieldtype': 'data',
	'reqd': 1
},)
std_columns_main = ({
		'fieldname': 'updated_on',
		'fieldtype': 'timestamp',
	},
	{
		'fieldname': 'created_by',
		'fieldtype': 'link',
		'options': 'Profile'
	},
	{
		'fieldname': 'created_on',
		'fieldtype': 'timestamp',
	},
	{
		'fieldname': 'updated_by',
		'fieldtype': 'link',
		'options': 'Profile'
	},
	{
		'fieldname': 'docstatus',
		'fieldtype': 'int',
	},
	{
		'fieldname': '_data',
		'fieldtype': 'text',
	})

	
std_columns_table = ({
		'fieldname': 'parent',
		'fieldtype': 'data',
	},
	{
		'fieldname': 'parenttype',
		'fieldtype': 'Link',
		'options': 'DocType'	
	},
	{
		'fieldname': 'parentfield',
		'fieldtype': 'Link'
	},
	{
		'fieldname': 'idx',
		'fieldtype': 'Integer',
		'length': 5
	})
	
type_map = {
	'currency':		('decimal', '18,6')
	,'int':		('int', '11')
	,'float':		('decimal', '18,6')
	,'check':		('int', '1')
	,'small text':	('smalltext', '')
	,'long text':	('longtext', '')
	,'code':		('text', '')
	,'text editor':	('text', '')
	,'date':		('date', '')
	,'time':		('time', '')
	,'timestamp':	('timestamp', '')
	,'text':		('text', '')
	,'data':		('varchar', '180')
	,'link':		('varchar', '180')
	,'password':	('varchar', '180')
	,'select':		('varchar', '180')
	,'read only':	('varchar', '180')
}


def create_table(conn, doctypeobj):
	"""make table based on given info"""
	import wn
	
	template = """create table `%s` (%s) ENGINE=InnoDB CHARACTER SET=utf8"""
	columns, constraints = [], []

	def column_def():
		"""make col definition from docfield"""
		if not d.get('fieldtype').lower() in type_map:
			return

		column_def.db_type, column_def.db_length = type_map[d.get("fieldtype").lower()]
		
		def set_length():
			"""set length if specifed or take default"""
			if column_def.db_length or d.get("length"):
				column_def.db_length = '(%s)' % str(column_def.db_length or d.get("length"))

		def set_defaults():
			"""set numeric types to default to 0"""
			if d.get('fieldtype').lower() in ('int', 'float', 'currency', 'check') and d.get('default')==None:
				d['default'] = 0
		
		def set_as_primary_key():
			"""set name as primary key unless specified as an index"""
			if d.get('fieldname')=='name' and (not 'name' in doctypeobj.get('indexes', [])):
				args['keys'] = ' primary key'

				# auto_increment
				if doctypeobj.get('autoname', '').lower()=='autonumber':
					args['fieldtype'] = 'mediumint'
					args['length'] = ''
					args['keys'] += ' auto_increment'

		def make_args():
			"""make column def commands"""
			return {
				"fieldtype": column_def.db_type,
				"length": column_def.db_length,
				"fieldname": d.get('fieldname'),
				"default": d.get("default")!=None and (' not null default "%s"' %\
				 	str(d.get('default')).replace('"', '\"')) or '',
				"keys": '',
				"not_null": d.get('reqd') and ' not null' or ''
			}
		
		def add_constraints():
			"""add constraints for links and indexes"""
			# constraints
			if d.get('fieldtype')=='Link':
				constraints.append('constraint foreign key `%s`(`%s`) references `%s`(name)' % \
					(d.get('fieldname'), d.get('fieldname'), d.get('options')))

			if d.get('index'):
				constraints.append('index `%s`(`%s`)' % (d.get('fieldname'), d.get('fieldname')))

		# start scrubbing
		set_length()
		set_defaults()
		args = make_args()
		set_as_primary_key()
		add_constraints()

		# add to columns
		columns.append('`%(fieldname)s` %(fieldtype)s%(length)s%(not_null)s%(default)s%(keys)s' % args)
		

	# add std columns
	if doctypeobj.get("std_fields") != "No":
		for d in std_columns:
			column_def()

		# is table
		for d in (doctypeobj.get('istable') and std_columns_table or std_columns_main):
			column_def()

	# fields
	for d in doctypeobj.get({"doctype":"DocField"}):
		column_def()
	
	# indexes
	for i in doctypeobj.get('indexes', []):
		constraints.append("index `%s`(%s)" % (wn.cs(i), i))
	
	# run the query!
	query = template % (wn.cs(doctypeobj.get('name')), ',\n'.join(columns + constraints))	
	
	#print query
	
	conn.sql("""set foreign_key_checks=0""")
	try:
		if wn.cs(doctypeobj.get('name')) in conn.get_tables():
			conn.sql("""drop table `%s`""" % wn.cs(doctypeobj.get('name')))
		conn.sql(query)
	finally:
		conn.sql("""set foreign_key_checks=1""")	

def remake_table(conn, doctypeobj):
	"""drop table and remake it, backing up the data first"""
	import utils, os
	
	name = doctypeobj.get('name')
	data = conn.sql("""select * from `%s`""" % wn.cs(name), as_dict=1)
	fname = utils.random_string(15) + '.txt'
	with open(fname, 'w') as tmpfile:
		tmpfile.write(str(data))
		
	conn.sql("""set foreign_key_checks=0""")
	conn.sql("""drop table `%s`""" % wn.cs(name))
	
	make_table(doctypeobj)
	conn.sql("""set foreign_key_checks=0""")	
	
	with open(fname, 'r') as tmpfile:
		mega_list = eval(tmpfile.read())
	
	for m in mega_list:
		conn.begin()
		conn.insert(m)
		conn.commit()
	
	conn.sql("""set foreign_key_checks=1""")
	os.remove(fname)
	



