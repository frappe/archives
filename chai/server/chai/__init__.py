# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license
# Authors: Rushabh Mehta (@rushabh_mehta)

request = None
response = None
session = None
db_session = None

def T(text):
	"""
	Translate the string in the given language
	"""
	from chai.utils.translate import translate
	translate(s)
	
def msg(text, with_exception=False):
	"""
	Send a message to be displayed to the user
	"""
	global response
	response.messages.append(T(text))
	if with with_exception:
		raise Exception
		
def notify(text):
	"""
	Send a notification to the user
	"""
	global response
	response.notifications.append(T(text))