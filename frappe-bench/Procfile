web: ./env/bin/frappe --serve --sites_path sites
worker: sh -c 'cd sites && exec ../env/bin/python -m frappe.celery_app worker'
workerbeat: sh -c 'cd sites && exec ../env/bin/python -m frappe.celery_app beat -s scheduler.schedule'
