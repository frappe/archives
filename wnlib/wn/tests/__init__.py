"""
Common test functions
"""

import wn, wn.model, wn.backends

def make_test_doctype():
	files = wn.backends.get('files')
	files.insert_doclist([{"doctype":"DocType", "name":"Test", 
		"controller":"wn.tests.test_controller.Test", "backend":"mysql"},
	{"doctype":"DocField", "fieldtype":"Data", "fieldname":"test_data", "reqd":1, "listable":1},
	{"doctype":"DocField", "fieldtype":"Date", "fieldname":"test_date"},
	{"doctype":"DocField", "fieldtype":"Text", "fieldname":"test_text"},
	{"doctype":"DocField", "fieldtype":"Int", "fieldname":"test_int", "listable":1},
	{"doctype":"DocField", "fieldtype":"Float", "fieldname":"test_float"},
	{"doctype":"DocField", "fieldtype":"Currency", "fieldname":"test_currency"},
	])
	wn.model.get('DocType', "Test").setup()
	
def cleanup_test():
	files = wn.backends.get('files').remove('DocType', 'Test')
