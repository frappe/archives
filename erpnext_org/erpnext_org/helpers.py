from __future__ import unicode_literals
import frappe, json

from erpnext_org.doctype.registrant.registrant import AlreadyRegistered

@frappe.whitelist(allow_guest=True)
def register(data):
	data = json.loads(data)

	r = frappe.new_doc("Registrant")
	for key in data:
		r.set(key, data[key])

	try:
		r.insert(ignore_permissions=True)
	except AlreadyRegistered:
		return "Already Registered. Please Email us at info@erpnext.com for any queries."

	frappe.sendmail(recipients=["info@erpnext.com"], sender="notifications@erpnext.com",
		subject="New Registrant", message=message.format(**data), bulk=True)

message = """
### Registrant Details

Name: {full_name}
<br>Company: {company_name}
<br>Email: {email_id}
<br>Comments: {comments}

User: {is_user}
<br>Partner: {is_partner}
<br>Developer: {is_developer}
"""
