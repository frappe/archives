"""translation lib"""

# translations langages
translations = {}
from itertools import chain
import os, json

def xgettext(lang):
	"""walk and extract views messages and write in the i18n folder"""
	
	# for framework
	all_messages = extract_from_files(chain(os.walk('lib/views'), os.walk('lib/lib_controllers'),
		os.walk('lib/client/wn')))
	all_messages += extract_from_doctypes(os.walk('lib/documents/doctype'))
	
	messages = write_i18n_file(os.path.join('lib', 'i18n', lang + '.json'), all_messages)

	# for app
	all_messages += extract_from_files(chain(os.walk('views'), os.walk('controllers')))
	all_messages += extract_from_doctypes(os.walk('models/doctype'))

	write_i18n_file(os.path.join('i18n', lang + '.json'), all_messages, messages)

	
def extract_from_files(walk):
	"""extract messages from file using primitive xgettext. In the long run,
	this should ideally be supplemented using xgettext. Does not implement
	fancy ideas like plural and maybe multi-line strings don't work"""
	import re
	messages = []
	for wt in walk:
		for fname in wt[2]:
			with open(os.path.join(wt[0], fname), 'r') as sourcefile:
				txt = sourcefile.read()
				messages += re.findall('_\("([^"]*)"\)', txt)
				messages += re.findall('_\("{3}([^"]*)"{3}\)', txt, re.S)
	
	return list(set(messages))

def extract_from_doctypes(walk):
	"""get labels, descriptions from doctype"""
	import wn.model
	messages = []
	for wt in walk:
		for fname in filter(lambda n: n.endswith('.json'), wt[2]):
			with open(os.path.join(wt[0], fname), 'r') as docfile:
				for d in json.loads(docfile.read()):
					if 'label' in d:
						messages.append(d.get('label'))
					if 'description' in d:
						messages.append(d.get('description'))

	return messages

def write_i18n_file(fpath, all_messages, messages=None):
	"""write i18n file at given fpath"""

	if not messages: messages = {}

	if not os.path.exists(os.path.dirname(fpath)):
		os.makedirs(os.path.dirname(fpath))

	# read existing file if exists
	if os.path.exists(fpath):
		with open(fpath, 'r') as langfile:
			set_messages = json.loads(langfile.read())
			# append pre-loaded messages
			for m in set_messages:
				if set_messages[m]:
					messages[m] = set_messages[m]
		
	with open(fpath, 'w') as langfile:
		for m in set(all_messages):
			if not m in messages:
				messages[m] = ""
		langfile.write(json.dumps(messages, indent=1, sort_keys=True).encode('utf-8'))
		
	return messages

def lang_path(lang):
	"""get path of language file relative to app root"""
	return os.path.join('i18n', lang + '.json')
	
def import_lang(lang):
	"""import a language file"""
	global translations
	import codecs
	
	if lang=='en':
		translations['en'] = {}
		return
	
	if not lang in translations:
		import json
		with codecs.open(os.path.join('i18n', lang + '.json'), 'r', 'utf-8') as src:
			translations[lang] = json.loads(src.read())
			
def _(txt):
	"""translate"""
	import wn
	import_lang(wn.lang)
	return translations.get(wn.lang, {}).get(txt) or txt
	
if __name__=='__main__':
	import sys
	sys.path.append('lib')
	sys.path.append('controllers')
	if len(sys.argv) < 2:
		print "Usage: python lib/wn/translate.py [lang]"
	else:
		xgettext(sys.argv[1])
