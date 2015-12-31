# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "team_frappe_io"
app_title = "Frappe Team"
app_publisher = "Frappe"
app_description = "team.frappe.io"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_version = "0.0.1"

required_apps = ["frappe_theme"]

website_context = {
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/frappe-icon.svg' />Frappé",
	"top_bar_items": [
		{"label":"Jobs", "url":"/jobs", "right": 1},
		{"label":"Press", "url":"/press", "right": 1},
		{"label":"Inspiration", "url":"/inspiration", "right": 1},
		{"label":"Blog", "url":"https://blog.frappe.io", "right": 1}
	],
	"hide_login": 1
}

fixtures = ["Contact Us Settings", "Web Form", "Email Alert"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/team_frappe_io/css/team_frappe_io.css"
# app_include_js = "/assets/team_frappe_io/js/team_frappe_io.js"

# include js, css files in header of web template
# web_include_css = "/assets/team_frappe_io/css/team_frappe_io.css"
# web_include_js = "/assets/team_frappe_io/js/team_frappe_io.js"

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

# before_install = "team_frappe_io.install.before_install"
# after_install = "team_frappe_io.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "team_frappe_io.notifications.get_notification_config"

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
# 		"team_frappe_io.tasks.all"
# 	],
# 	"daily": [
# 		"team_frappe_io.tasks.daily"
# 	],
# 	"hourly": [
# 		"team_frappe_io.tasks.hourly"
# 	],
# 	"weekly": [
# 		"team_frappe_io.tasks.weekly"
# 	]
# 	"monthly": [
# 		"team_frappe_io.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "team_frappe_io.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "team_frappe_io.event.get_events"
# }
