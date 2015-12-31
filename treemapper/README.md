Tree Census Tool for TreeMapIndia
---

### To Do

- Integrate app into page
- Fix login
- Make tree pages from generator
- Make recently added trees from generator

### Build on webnotes/wnframework

Install

	$ git clone git@github.com:webnotes/wnframework lib
	$ git clone git@github.com:webnotes/treemapper app
	$ lib/wnf.py --make_conf
	$ lib/wnf.py --reinstall
	$ lib/wnf.py --build

### Pre-requisites

1. MySQL
1. Python
1. Python Libraries
	1. MySQLdb
	1. Jinja2
	1. requests

#### Export

Before pushing, export install fixtures

	$ python app/startup/install_fixtures/export_fixtures.py
