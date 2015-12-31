# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "kb_frappe_io"
app_title = "Frappe KB"
app_publisher = "Frappe"
app_description = "kb.frappe.io"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_version = "0.0.1"

required_apps = ["knowledge_base", "frappe_theme"]

website_context = {
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/frappe-icon.svg' />Frappé Knowledge Base",
	"top_bar_items": [
		{"label": "Frappe Tutorial", "url": "https://frappe.io/tutorial", "target": "_blank"},
		{"label": "Frappe Developer Reference", "url": "https://docs.frappe.io", "target": "_blank"},
	],
	"hide_login": 1,
	"hero": {
		"kb": "templates/includes/hero.html"
	},
	"page_titles": {
		"kb": "Frappé Knowledge Base"
	},
	"home_page": "/kb"
}


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kb_frappe_io/css/kb_frappe_io.css"
# app_include_js = "/assets/kb_frappe_io/js/kb_frappe_io.js"

# include js, css files in header of web template
# web_include_css = "/assets/kb_frappe_io/css/kb_frappe_io.css"
# web_include_js = "/assets/kb_frappe_io/js/kb_frappe_io.js"

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

# before_install = "kb_frappe_io.install.before_install"
# after_install = "kb_frappe_io.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kb_frappe_io.notifications.get_notification_config"

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
# 		"kb_frappe_io.tasks.all"
# 	],
# 	"daily": [
# 		"kb_frappe_io.tasks.daily"
# 	],
# 	"hourly": [
# 		"kb_frappe_io.tasks.hourly"
# 	],
# 	"weekly": [
# 		"kb_frappe_io.tasks.weekly"
# 	]
# 	"monthly": [
# 		"kb_frappe_io.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "kb_frappe_io.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "kb_frappe_io.event.get_events"
# }

fixtures = ["Contact Us Settings"]
