import wn, wn.model, wn.backends

install_docs = [
	{"doctype": "Role", "name": "Mail User"},
	{'doctype':'User Role', 'user': 'Administrator', 'role': 'Mail User'},
	{'doctype':'Mail Account', 'name':'Administrator', 'email_service':'GMail',
		'username':'setusername', 'password':'setpassword',
		'imap_server':'imap.gmail.com', 'imap_port':993, 'imap_ssl':1,
		'smtp_server':'smtp.gmail.com', 'smtp_port':587, 'smtp_ssl':1},
	{'doctype':'Mail Service', 'service_name':'Facebook', 'name':'Facebook', 
		'global':'Yes', 'from':'facebookmail.com'},
	{'doctype':'Mail Service', 'service_name':'LinkedIn', 'name':'LinkedIn', 
		'global':'Yes', 'from':'linkedin.com'},
	{'doctype':'Mail Service', 'service_name':'Twitter', 'name':'Twitter', 
		'global':'Yes', 'from':'twitter.com'},
	{'doctype':'Mail Service', 'service_name':'Google Alerts', 'name':'Google Alerts', 
		'global':'Yes', 'from':'googlealerts'},
	{'doctype':'Mail Service', 'service_name':'Groups', 'name':'Groups', 
		'global':'Yes', 'from': 'yahoogroups.com', 'reply_to':'googlegroups.com,yahoogroups.com'}
]

def module_init():
	wn.backends.get('mysql').begin()
	#
	wn.backends.get('mysql').commit()

def execute():
	wn.backends.get('mysql').begin()
	for d in install_docs:
		wn.model.new(d).insert()
		
	wn.backends.get('mysql').commit()
		
