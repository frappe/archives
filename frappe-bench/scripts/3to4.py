from frappe.installer import add_to_installed_apps
from frappe.cli import latest
from frappe.modules.patch_handler import executed
import frappe
import argparse
import os

sites_path = os.environ.get('SITES_PATH', 'sites')
last_3_patch = 'patches.1401.fix_planned_qty'

def validate(site):
	frappe.init(site=site, sites_path=sites_path)
	frappe.connect()
	if not executed(last_3_patch):
		raise Exception, "site not ready to migrate to version 4"
	frappe.destroy()


def migrate(site):
	validate(site)
	frappe.init(site=site, sites_path=sites_path)
	frappe.connect()
	add_to_installed_apps('frappe', rebuild_website=False)
	add_to_installed_apps('erpnext', rebuild_website=False)
	add_to_installed_apps('shopping_cart', rebuild_website=False)
	latest()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('site')
	args = parser.parse_args()
	migrate(args.site)
