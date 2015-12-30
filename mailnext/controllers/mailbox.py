import webnotes

@webnotes.whitelist()
def get_mails():
	"""list of mails"""
	args = webnotes.form_dict
	if args['service_name'] == 'Mails':
		cond = 'ifnull(mail_service, "")=""'
	else:
		cond = 'ifnull(mail_service, "")="%s"' % args['service_name'].replace('"', '\"')
	
	if args.get('hard_refresh'):
		import imap
		imap.IMAP().fetch_new_mails()
		
	return webnotes.conn.sql("""select * from `tabMail Message` where
		mail_account = "%s" and
		%s order by uid desc limit %s, %s""" % (webnotes.session['user'], cond,
		args.get('limit_start'), args.get('limit_page_length')), as_dict=1)
