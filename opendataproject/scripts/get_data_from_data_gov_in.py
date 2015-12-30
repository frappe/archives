from __future__ import unicode_literals
import requests, re, os, csv, json, urllib2
from utils import convert_to_csv

import webnotes

sources = [
	"http://data.gov.in/catalogs"
]

# don't downloads datasets larger than:
max_file_size_in_kb = 300

def download():
	sourcepath = os.path.join("app", "downloads", "data.gov.in")

	not os.path.exists(sourcepath) and os.makedirs(sourcepath)
	
	for i in range(415)[165:]:
		print "for page %s" % i
		response = requests.get(sources[0] + "?page=%s" % i, verify=False)
		page_properties = get_url_title_and_description_from_html(response.text)
				
		for filename, properties in page_properties.iteritems():
			filepath = os.path.join(sourcepath, filename)
			filecontent = ""
			print "downloading " + filename
			if not os.path.exists(filepath):
				try:
					url = urllib2.urlopen(properties["url"].encode("utf-8"))
					size = url.headers["Content-Length"]
					if int(size) < int(max_file_size_in_kb * 1024):
						r = requests.get(properties["url"])
						with open(filepath, "w") as datafile:
							for chunk in r.iter_content(1024):
								datafile.write(chunk)
					else:
						print "[ignored] [too big] %s (%s)" % (filename, size)
				except urllib2.HTTPError, e:
					print e
			
			if os.path.exists(filepath):
				if filepath.split(".")[-1]=="xls":
					try:
						files = convert_to_csv(filepath, sourcepath)

						# remove orignal xls file (not needed)
						os.remove(filepath)

						# keep as a marker that this file is downloaded
						os.system("touch %s" % filepath)
					except Exception, e:
						files = []
						print e
				else:
					files = [filepath]
			
			for fpath in files:
				prepend_property_headers(fpath, properties)

def prepend_property_headers(fpath, properties):
	with open(fpath, "r") as csvfile:
		data = csvfile.read()

	with open(fpath, "w") as csvfile:
		csvfile.write("-----\n")
		csvfile.write(json.dumps(properties, indent=1, sort_keys=True))
		csvfile.write("\n-----\n")
		csvfile.write(data)

def get_url_title_and_description_from_html(text):
	properties = {}
	
	text = text.split("<tbody>")[1].split("</tbody>")[0]
		
	for row in text.split("<tr")[1:]:
		row = row.replace("\n", "")
		url = re.findall("url=([^&]+)", row)[0]
		file_name = url.split("/")[-1]
		if file_name.split(".")[-1] in ("csv", "xls"):
			properties[file_name] = {
				"file_name": file_name,
				"url": url,
				"title": re.findall('title="([^"]+)"', row)[0],
				"description": re.findall("<br/>([^<]+)", row)[0]
			}
	return properties
		

if __name__=="__main__":
	download()
