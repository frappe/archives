# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# GNU General Public License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = True

def on_login(login_manager):
	agent = frappe.db.get_value("Website Chat Agent",
		{"user": frappe.session.user }, ["name", "status"], as_dict=True)
	if agent and agent.status=="Offline":
		agent = frappe.get_doc("Website Chat Agent", agent.name)
		agent.status = "Active"
		agent.save(ignore_permissions=True)

def get_context(context):
	return {
		"title": _("Chat")
	}

@frappe.whitelist(allow_guest=True)
def get_agent_status():
	out = {}
	if frappe.get_list("Website Chat Agent", filters={"status":"Active"},
		ignore_permissions=True, limit_page_length=1):
		out["agent_status"] = "active"
	else:
		out["agent_status"] = "offline"

	if frappe.session.user!="Guest":
		# check if signed-in user is agent
		my_status = frappe.db.get_value("Website Chat Agent", {
			"user": frappe.session.user }, "status")

		if my_status:
			out["my_status"] = my_status
			# send active chats
			out["active_sessions"] = get_active_sessions()

	return out

@frappe.whitelist(allow_guest=True)
def get_latest(chatid, sender, last_message_id=""):
	out = {}
	if chatid != "no-chat":
		doc = frappe.cache().get_value(chatid)
		if not doc:
			doc = frappe.get_doc("Website Chat Session", chatid)
			frappe.cache().set_value(chatid, doc)

		out["messages"] = []
		for d in doc.get("website_chat_messages"):
			if d.get("name") > last_message_id:
				out["messages"].append(d)

		out["status"] = doc.get('status')

	if sender=="Agent":
		out["active_sessions"] = get_active_sessions()

	return out

@frappe.whitelist()
def get_active_sessions():
	# memcache this
	active_sessions = frappe.cache().get_value("website-chat-active-sessions")
	if active_sessions==None:
		active_sessions = frappe.get_list("Website Chat Session",
			fields=["name", "client_name", "status"],
			filters={"status":("in", ("Active", "New", "Waiting"))},
			order_by="creation desc")
		frappe.cache().set_value("website-chat-active-sessions", active_sessions)

	return active_sessions

@frappe.whitelist(allow_guest=True)
def end_chat(chatid):
	chat = frappe.get_doc("Website Chat Session", chatid)
	chat.status = "Ended"
	chat.save(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def set_feedback(chatid, feedback):
	frappe.db.set_value("Website Chat Session", chatid, "feedback", feedback)

@frappe.whitelist()
def set_agent_status(my_status):
	agent = frappe.get_doc("Website Chat Agent", {"user": frappe.session.user})
	if my_status=="Active":
		agent.status = "Offline"
	else:
		agent.status = "Active"
	agent.save(ignore_permissions=True)
	return agent.status
