# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "kb_erpnext_com"
app_title = "ERPNext KB"
app_publisher = "Frappe"
app_description = "kb.erpnext.com"
app_icon = "icon-book"
app_color = "green"
app_email = "info@frappe.io"
app_version = "0.0.1"

required_apps = ["knowledge_base", "frappe_theme"]

website_context = {
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/erp-icon.svg' />ERPNext Knowledge Base",
	"top_bar_items": [
		{"label": "ERPNext Manual", "url": "https://manual.erpnext.com"},
		{"label": "ERPNext Developer Reference", "url": "https://docs.erpnext.com"},
	],
	"hide_login": 1,
	"hero": {
		"kb": "templates/includes/hero.html"
	},
	"page_titles": {
		"kb": "ERPNext Knowledge Base"
	},
	"home_page": "/kb",
	"favicon": "/assets/frappe_theme/img/favicon.ico",
}


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kb_erpnext_com/css/kb_erpnext_com.css"
# app_include_js = "/assets/kb_erpnext_com/js/kb_erpnext_com.js"

# include js, css files in header of web template
# web_include_css = "/assets/kb_erpnext_com/css/kb_erpnext_com.css"
# web_include_js = "/assets/kb_erpnext_com/js/kb_erpnext_com.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "kb_erpnext_com.install.before_install"
# after_install = "kb_erpnext_com.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kb_erpnext_com.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"kb_erpnext_com.tasks.all"
# 	],
# 	"daily": [
# 		"kb_erpnext_com.tasks.daily"
# 	],
# 	"hourly": [
# 		"kb_erpnext_com.tasks.hourly"
# 	],
# 	"weekly": [
# 		"kb_erpnext_com.tasks.weekly"
# 	]
# 	"monthly": [
# 		"kb_erpnext_com.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "kb_erpnext_com.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "kb_erpnext_com.event.get_events"
# }

fixtures = ["Contact Us Settings"]
