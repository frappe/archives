# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "conf_erpnext_com"
app_title = "ERPNext Conf"
app_publisher = "Frappe"
app_description = "conf.erpnext.com"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_version = "0.0.1"

required_apps = ["frappe_theme"]

website_context = {
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/erp-icon.svg' />ERPNext Conference",
	# "top_bar_items": [
	# 	{"label": "Conf 2014", "url": "/2014", "right": 1}
	# ],
	"hide_login": 1,
	"favicon": "/assets/frappe_theme/img/favicon.ico"
}


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/conf_erpnext_com/css/conf_erpnext_com.css"
# app_include_js = "/assets/conf_erpnext_com/js/conf_erpnext_com.js"

# include js, css files in header of web template
# web_include_css = "/assets/conf_erpnext_com/css/conf_erpnext_com.css"
# web_include_js = "/assets/conf_erpnext_com/js/conf_erpnext_com.js"

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

# before_install = "conf_erpnext_com.install.before_install"
# after_install = "conf_erpnext_com.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "conf_erpnext_com.notifications.get_notification_config"

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
# 		"conf_erpnext_com.tasks.all"
# 	],
# 	"daily": [
# 		"conf_erpnext_com.tasks.daily"
# 	],
# 	"hourly": [
# 		"conf_erpnext_com.tasks.hourly"
# 	],
# 	"weekly": [
# 		"conf_erpnext_com.tasks.weekly"
# 	]
# 	"monthly": [
# 		"conf_erpnext_com.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "conf_erpnext_com.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "conf_erpnext_com.event.get_events"
# }

fixtures = ["Contact Us Settings"]
