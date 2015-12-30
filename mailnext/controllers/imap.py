# on refresh, search all mails since last update
# get BODY.PEEK[HEADER] BODY.PEEK[TEXT] FLAGS for these mails
# push header into email lib
# update the Mail table

# for each mail account, we must know login details, last update

# flags - seen, answered, flagged, deleted

class IMAP:
	def __init__(self):
		self.connect()

	def connect(self):
		"""connect from user's mailbox"""
		import webnotes
		from webnotes.model.doc import Document
		d = Document('Mail Account', webnotes.session['user'])
	
		from imapclient import IMAPClient
		
		self.conn = IMAPClient(str(d.imap_server) or 'imap.gmail.com', use_uid=True, ssl=True)
		self.conn.login(str(d.username), str(d.password))
		
		self.conn.select_folder('INBOX')
		self.setup_services()

	def disconnect(self):
		self.conn.logout()

	def sync(self):
		"""get last emails and sync flags"""
		self.get_new_mails()
		self.sync_flags()
	
	def new_mails_since(self):
		"""fetch new mails since last update or 7 days"""
		pass

	def max_uid(self):
		"""get last mail"""
		import webnotes
		return webnotes.conn.sql("""select max(uid) from `tabMail Message` 
			where mail_account=%s""", webnotes.session['user'])[0][0] or ''
	
	def get_new_mail_uids(self, days=7):
		import datetime
		
		max_uid = self.max_uid()
		if max_uid:
			uid_range = 'UID {uid}:*'.format(uid=str(int(max_uid)+1))
			return self.conn.search([uid_range])
		else:
			date = (datetime.date.today() - datetime.timedelta(days)).strftime("%d-%b-%Y")
			return self.conn.search(['SINCE {date}'.format(date=date)])

	def fetch_new_mails(self):
		"""fetch flags header and body for new mails"""
		uid_list = self.get_new_mail_uids()
		
		fetch = self.conn.fetch(uid_list, ['FLAGS', 'BODY.PEEK[HEADER]'])
		
		for uid in uid_list:
			self.add_mail(uid, fetch[uid]['FLAGS'], fetch[uid]['BODY[HEADER]'])
		
			
	def add_mail(self, uid, flags, headers):
		"""add to table"""
		import webnotes
		
		if webnotes.conn.exists('Mail Message', uid):
			return
			
		import email, datetime
		from email.utils import parsedate
		from webnotes.model.doc import Document

		msg = email.message_from_string(headers)

		d = Document('Mail Message')
		d.owner = webnotes.session['user']
		d.mail_account = d.owner
		d.uid = str(uid)
		d.name = d.uid
		d.fields['from'] = msg['From']
		d.fields['to'] = msg['To']
		d.reply_to = msg.get('Reply-To')
		d.cc = msg.get('Cc')
		d.subject = msg.get('Subject')

		d.date = datetime.datetime(*parsedate(msg['Date'])[:6]).strftime('%Y-%m-%d %H:%M:%S')
		
		d.mail_service = self.guess_service(msg)
		self.set_flags(d, flags)
		
		webnotes.conn.begin()
		d.save()
		webnotes.conn.commit()
	
	def setup_services(self):
		"""make list of services"""
		import webnotes
		self.services = webnotes.conn.sql("""select * from `tabMail Service`""", as_dict=1)
	
	def guess_service(self, msg):
		"""guess service"""
		for s in self.services:
			for check_id in (s.get('from') or '').split(','):
				if check_id and check_id in (msg['From'] or ''):
					return s['service_name']

			for check_id in (s.get('reply_to') or '').split(','):
				if check_id and check_id in (msg.get('Reply-To') or ''):
					return s['service_name']
					
		return ''

	def set_flags(self, d, flags):
		"""read flags"""
		import imapclient
		d.seen = imapclient.SEEN in flags and 1 or 0
		d.answered = imapclient.ANSWERED in flags and 1 or 0
		d.deleted = imapclient.DELETED in flags and 1 or 0
		d.flagged = imapclient.FLAGGED in flags and 1 or 0
		#d.notjunk = 
		
import unittest
class TestIMAP(unittest.TestCase):
	def setUp(self):
		self.mbox = IMAP()
	def tearDown(self):
		self.mbox.disconnect()
	def testFetch(self):
		self.mbox.fetch_new_mails()
		self.assertTrue(True)

if __name__=='__main__':
	import sys
	sys.path.append('.')
	sys.path.append('lib/py')
	import webnotes
	webnotes.connect()
	unittest.main()
