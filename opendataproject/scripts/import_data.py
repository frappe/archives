from __future__ import unicode_literals

import sys
sys.path = ['.', 'lib', 'app'] + sys.path

import webnotes, utils, MySQLdb, os, json, re

exclude_from_headers = {
	"Download XLS for ": "",
	"Download CSV for ": "",
	"(External Link that opens in a new window)": "",
	" - ": "-",
	"%": "percent",
	",": " ",
	"#": " ",
	"/": "-",
	"&amp;": "and"
}

def import_data():
	print "building state and district masters..."
	
	webnotes.conn.sql("delete from `tabData Set`");
	
	webnotes.conn.auto_commit_on_many_writes = True
	for fname in os.listdir(os.path.join("app", "downloads", "data.gov.in")):
		if fname.endswith(".csv"):
			fpath = os.path.join("app", "downloads", "data.gov.in", fname)
			print fname
			add_values(fname, fpath)
		

def add_values(fname, fpath):
	headers, data = utils.get_file_data(fpath)
	if not data:
		return

	if not headers["title"]:
		return

	add_regions(data)
	
	for key, value in exclude_from_headers.iteritems():
		headers["title"] = headers["title"].replace(key, value)

	data_set = headers["title"][:170].replace(" ", "-").lower()

	if not webnotes.conn.exists("Data Set", data_set):
		try:
			webnotes.bean({
				"doctype": "Data Set",
				"name": data_set,
				"title": headers["title"],
				"description": headers["description"],
				"raw_filename": fname,
				"url": headers["url"],
				"source": "data.gov.in",
				"row_count": len(data),
				"__islocal": 1
			}).save()
		except MySQLdb.IntegrityError, e:
			pass
			
	webnotes.conn.commit()
	
def add_regions(data):
	def scrub(text):
		text = text.strip().title()

		for w in ("Total", "State", "Grand"):
			if w in text:
				return ""

		text = re.sub("\([^)]\)", "", text)
		text = re.sub("D[ .]*and[ .]*N", "Dadra and Nagar", text)
		text = re.sub("Ch[h]*at[t]*isgarh", "Chattisgarh", text.replace(" ", "").title())
		text = re.sub("J[ .]*&[ .]*K", "Jammu & Kashmir", text)
		text = re.sub("A[ .]*&[ .]*N", "Andaman & Nicobar", text)
		text = re.sub("Andaman[ .]*&[ .]*Nicobar[s ]*\w*", "Andaman & Nicobar Islands", text)
		
		return text
		
	if data[0][0].lower()=="state":
		states = list(set(d[0] for d in data[1:]))
		for d in states:
			name = scrub(d)
			if name and not webnotes.conn.exists("Region", name):
				webnotes.bean({"doctype":"Region", "region_type":"State", 
					"name": name }).insert()
					
		webnotes.conn.commit()
					
		if data[0][1].lower()=="district":
			for row in data[1:]:
				name = scrub(row[1])
				if name and row[1] and not webnotes.conn.exists("Region", name):
					webnotes.bean({"doctype": "Region", "region_type":"District", 
						"parent_region": scrub(row[0]), "name": name }).insert()
					
			webnotes.conn.commit()

eliminate_list = (".", "'s", "'", "*")
replace_with_space = (".", ",", ";", ":", "-", "/", "(", ")")
common_list = ("Refers", "Provides", "Details", "Constant", "According", "During", "Schemes", 
	"Approved", "Consists", "Number", "Arrived", "Through")

def make_word_map():
	webnotes.conn.sql("""delete from tabWord""")
	webnotes.conn.sql("""delete from `tabWord Data Set`""")
	webnotes.conn.commit()
	webnotes.conn.auto_commit_on_many_writes = True
	for d in webnotes.conn.sql("""select name, ifnull(title, "") as title, 
		ifnull(description, "") as description 
		from `tabData Set`""", as_dict=True):
		sys.stdout.write(".")
		sys.stdout.flush()

		# cleanup
		all_text = d.title + d.description
		all_text = all_text.replace("%", "percent").replace('"', "")
		for t in replace_with_space:
			all_text = all_text.replace(t, " ")
		for t in eliminate_list:
			all_text = all_text.replace(t,"")

		for word in all_text.split():
			name = word.title()
			if len(name) > 5 and (name not in common_list):
				if not webnotes.conn.exists("Word", name):
					webnotes.doc({"doctype": "Word", "name": name, "count": 1}).insert()
				else:
					webnotes.conn.sql("""update tabWord set `count`=`count` + 1 where name=%s""", name)
					
				if not webnotes.conn.sql("""select name from `tabWord Data Set` 
					where word=%s and data_set=%s""", (name, d.name)):
					webnotes.doc({"doctype": "Word Data Set", "data_set": d.name, "word": name}).insert()
	
	for d in webnotes.conn.sql("select name from tabWord where `count`< 100"):
		webnotes.delete_doc('Word', d[0])
	
	webnotes.conn.commit()

def make_word_count():
	for ds in webnotes.conn.sql("""select name, raw_filename from `tabData Set`""", as_dict=1):
		from webnotes.utils import get_path
		
		if ds.raw_filename:
			headers, data = utils.get_file_data(get_path("app", "downloads", 
				"data.gov.in", ds.raw_filename))
			
			webnotes.conn.set_value("Data Set", ds.name, "row_count", len(data))
	
	webnotes.conn.commit()
	
if __name__=="__main__":
	webnotes.connect()
	webnotes.init()
	import_data()
	make_word_map()
	make_word_count()
	