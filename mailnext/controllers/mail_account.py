import webnotes
from webnotes.model.doclist import DocList

class MailAccount(DocList):
	def autoname(self):
		if not self.doc.name:
			self.doc.name = webnotes.session['user']
			
	def validate(self):
		"""update gmail / yahoo etc settings"""
		preset = {
			"GMail": {
				"imap_server":"imap.gmail.com",
				"imap_port": 993,
				"imap_ssl": 1,
				"smtp_server": "smtp.gmail.com",
				"smtp_port": 587,
				"smtp_ssl": 1
			},
		}
		if self.doc.email_service!='Other':
			self.doc.fields.update(preset[self.doc.email_service])
