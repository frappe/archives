## ERPNext Conf

conf.erpnext.com

### Install

Install Frappe Bench: https://github.com/frappe/bench

Step 1. Create a new site on the bench

```
$ bench new-site conf.erpnext.com
```

Step 2. Then install the app in the bench

```
$ bench get-app conf_erpnext_com git@github.com:frappe/conf_erpnext_com
```

Step 3: Then install the app in the site

```
$ bench --site conf.erpnext.com install-app conf_erpnext_com
```

Step 4: Start the bench

```
$ bench --site conf.erpnext.com serve --port 8000
```

Open your browser on `http://localhost:8000` to see the site


#### To develop

Disable website caching

1. Open `sites/conf.erpnext.com/site_config.json`
2. Add `"disable_website_cache": 1` to the options
3. Clear the cache: `bench --site conf.erpnext.com clear-cache`

Run `$ bench --site conf.erpnext.com serve --port 8000` again

Edits will appear on the site.

#### License

MIT
