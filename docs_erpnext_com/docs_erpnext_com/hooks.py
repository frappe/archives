# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "docs_erpnext_com"
app_title = "ERPNext Docs"
app_publisher = "Frappe"
app_description = "docs.erpnext.com"
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
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/erp-icon.svg' />ERPNext API Reference",
	"top_bar_items": [
		{"label": "Models", "url":"/current/models", "right": 1},
		{"label": "API", "url":"/current/api", "right": 1},
		{"label": "Articles", "url": "https://kb.erpnext.com", "target": "_blank", "right": 1},
		{"label": "Frappe Docs", "url": "https://docs.frappe.io", "target": "_blank", "right": 1},
		{"label": "Forum", "url":"https://discuss.erpnext.com", "target": "_blank", "right": 1},
	],
	"hide_login": 1,
	"js_globals": {
		"search_path": "/search"
	},
	"favicon": "/assets/frappe_theme/img/favicon.ico",
}

autodoc = {
	"for_app": "erpnext",
	"docs_app": "docs_erpnext_com"
}


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/docs_erpnext_com/css/docs_erpnext_com.css"
# app_include_js = "/assets/docs_erpnext_com/js/docs_erpnext_com.js"

# include js, css files in header of web template
# web_include_css = "/assets/docs_erpnext_com/css/docs_erpnext_com.css"
# web_include_js = "/assets/docs_erpnext_com/js/docs_erpnext_com.js"

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

# before_install = "docs_erpnext_com.install.before_install"
# after_install = "docs_erpnext_com.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "docs_erpnext_com.notifications.get_notification_config"

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
# 		"docs_erpnext_com.tasks.all"
# 	],
# 	"daily": [
# 		"docs_erpnext_com.tasks.daily"
# 	],
# 	"hourly": [
# 		"docs_erpnext_com.tasks.hourly"
# 	],
# 	"weekly": [
# 		"docs_erpnext_com.tasks.weekly"
# 	]
# 	"monthly": [
# 		"docs_erpnext_com.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "docs_erpnext_com.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "docs_erpnext_com.event.get_events"
# }

fixtures = ["Contact Us Settings"]
