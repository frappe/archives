# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "blog_frappe_io"
app_title = "Frappe Blog"
app_publisher = "Frappe"
app_description = "blog.frappe.io"
app_icon = "icon-book"
app_color = "green"
app_email = "info@frappe.io"
app_version = "0.0.1"

website_context = {
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/frappe-icon.svg' />Frappé Blog",
	# "top_bar_items": [
	# 	{"label": "About", "url":"/about", "right":1}
	# ],
	"hide_login": 1,
	"include_search": 1
}


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/blog_frappe_io/css/blog_frappe_io.css"
# app_include_js = "/assets/blog_frappe_io/js/blog_frappe_io.js"

# include js, css files in header of web template
# web_include_css = "/assets/blog_frappe_io/css/blog_frappe_io.css"
# web_include_js = "/assets/blog_frappe_io/js/blog_frappe_io.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "index"

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

# before_install = "blog_frappe_io.install.before_install"
# after_install = "blog_frappe_io.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "blog_frappe_io.notifications.get_notification_config"

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
# 		"blog_frappe_io.tasks.all"
# 	],
# 	"daily": [
# 		"blog_frappe_io.tasks.daily"
# 	],
# 	"hourly": [
# 		"blog_frappe_io.tasks.hourly"
# 	],
# 	"weekly": [
# 		"blog_frappe_io.tasks.weekly"
# 	]
# 	"monthly": [
# 		"blog_frappe_io.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "blog_frappe_io.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "blog_frappe_io.event.get_events"
# }

fixtures = ["Contact Us Settings"]
