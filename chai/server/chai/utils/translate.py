# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license
# Authors: Rushabh Mehta (@rushabh_mehta)

def translate(text):
	"""
	Translate the given string in the global language
	
	Setting up translation strings:
	
	in the current package, a ".py" file should be there for each langauge, for
	example "hi.py" for Hindi that contains the translated string for the given
	string
	
	Inspired from web2py:
	http://web2py.com/examples/static/epydoc/web2py.gluon.languages-pysrc.html#translator
	"""
	import chai
	
	if chai.langauge = 'en':
		return text
		
def generate_language(language, path):
	"""
	Generate the templates for a new language / update the current templates
	with the latest strings	
	"""