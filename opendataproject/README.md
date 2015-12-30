## Open Data Project

Viewer for Open Data in India. Based on wnframework

##### Install

1. Install MySQL with developer libs

		$ apt-get install MySQL-devel
		$ yum install MySQL-devel
		
1. Install

		$ mkdir opendataproject
		$ cd opendataproject
		$ git clone git@github.com:webnotes/opendataproject app
		$ git clone git@github.com:webnotes/wnframework lib
		$ cd lib && git checkout wsgi && cd lib..
		$ sudo pip install -r lib/requirements.txt
		$ lib/wnf.py --make_conf
		$ lib/wnf.py --reinstall
		$ python lib/webnotes/app.py 9000
	
1. Go to your browser localhost:9000

##### To Do

1. Download, extract and import data from data.gov.in
1. Build generators for regions, masters