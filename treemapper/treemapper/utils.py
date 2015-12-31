# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals

import webnotes
import pygeoip
from webnotes.utils import get_path

@webnotes.whitelist(allow_guest=True)
def get_city():
	p = pygeoip.GeoIP(get_path("app", "data", "GeoLiteCity.dat"))
	try:
		r = p.record_by_addr(webnotes.get_request_header("REMOTE_ADDR"))
	except Exception, e:
		r = {
			"city": "Mumbai",
			"latitude": "18.974999999999994",
			"longitude": "72.82579999999999"
		}
		
	return {k:v for k, v in r.iteritems() if k in ("city", "latitude", "longitude")}