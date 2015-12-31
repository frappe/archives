# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# GNU General Public License. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document

class WebsiteChatSession(Document):
	
	def validate(self):
		last_message_by = self.get("website_chat_messages")
		
		if last_message_by:
			last_message_by = last_message_by and last_message_by[-1].get("owner")

			if self.status=="Active" and last_message_by==self.client_email_id:
				self.status = "Waiting"
			elif self.status in ("Waiting", "New") and last_message_by!=self.client_email_id:
				self.status = "Active"
			
	def on_update(self):
		frappe.cache().delete_value("website-chat-active-sessions")
		frappe.cache().set_value(self.name, self)