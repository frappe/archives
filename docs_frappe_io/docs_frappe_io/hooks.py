# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "docs_frappe_io"
app_title = "Frappe Docs"
app_publisher = "Frappe"
app_description = "docs.frappe.io"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_version = "0.0.1"

required_apps = ["frappe_theme"]

website_route_rules = [
	{"from_route": "/search", "to_route": "Web Page"}
]

website_context = {
	"nav_home": "/v5.x",
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/frappe-icon.svg' />Frappé API Reference",
	"top_bar_items": [
		{"label": "Models", "url":"/current/models", "right": 1},
		{"label": "API", "url":"/current/api", "right": 1},
		{"label": "Articles", "url": "https://kb.frappe.io", "target": "_blank", "right": 1},
		{"label": "ERPNext Docs", "url": "https://docs.erpnext.com", "target": "_blank", "right": 1},
		{"label": "Forum", "url":"https://discuss.erpnext.com", "target": "_blank", "right": 1},
	],
	"hide_login": 1,
	"js_globals": {
		"search_path": "/search"
	},
}

autodoc = {
	"for_app": "frappe",
	"docs_app": "docs_frappe_io"
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/docs_frappe_io/css/docs_frappe_io.css"
# app_include_js = "/assets/docs_frappe_io/js/docs_frappe_io.js"

# include js, css files in header of web template
# web_include_css = "/assets/docs_frappe_io/css/docs_frappe_io.css"
# web_include_js = "/assets/docs_frappe_io/js/docs_frappe_io.js"

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

# before_install = "docs_frappe_io.install.before_install"
# after_install = "docs_frappe_io.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "docs_frappe_io.notifications.get_notification_config"

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
# 		"docs_frappe_io.tasks.all"
# 	],
# 	"daily": [
# 		"docs_frappe_io.tasks.daily"
# 	],
# 	"hourly": [
# 		"docs_frappe_io.tasks.hourly"
# 	],
# 	"weekly": [
# 		"docs_frappe_io.tasks.weekly"
# 	]
# 	"monthly": [
# 		"docs_frappe_io.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "docs_frappe_io.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "docs_frappe_io.event.get_events"
# }

fixtures = ["Contact Us Settings"]
