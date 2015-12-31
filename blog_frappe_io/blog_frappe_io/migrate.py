import frappe
from frappe.frappeclient import FrappeClient

def migrate():
	print "connecting..."
	frappe.flags.mute_emails = True
	remote = FrappeClient("https://frappe.io", "Administrator", frappe.conf.frappe_admin_password)
	remote.migrate_doctype("Blog Category")
	remote.migrate_doctype("Blogger")
	remote.migrate_doctype("Blog Post")
	frappe.flags.mute_emails = False
