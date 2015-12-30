#!/usr/bin/env python

from __future__ import unicode_literals
import os, time
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

jenv = Environment(loader = FileSystemLoader("templates"))
base_template = None
template_path = "templates/base.html"
file_timestamps = {}

while True:
	if os.stat(template_path).st_mtime != file_timestamps.get(template_path):
		# template updated
		file_timestamps = {
			template_path: os.stat(template_path).st_mtime
		}
		base_template = jenv.get_template("base.html")
		
	for fname in os.listdir("src"):
		if fname.endswith("md"):
			src_path = "src/" + fname
			if os.stat(src_path).st_mtime != file_timestamps.get(src_path):
				file_timestamps[src_path] = os.stat(src_path).st_mtime
				with open("src/" + fname, "r") as srcfile:
					html_fname = fname.split(".")[0] + ".html"
					with open(html_fname, "w") as htmlfile:
						args = {
							"content": markdown(srcfile.read())
						}
						print "writing " + html_fname
						htmlfile.write(base_template.render(args))
	time.sleep(2)