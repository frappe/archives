# Chai Project 0.1
# (c) 2011 Web Notes Technologies
# Chai Project may be freely distributed under MIT license
# Authors: Rushabh Mehta (@rushabh_mehta)

class Column:
	"""
	Wrapper around a table column
	"""
	def __init__(self, table, column_name):
		self.table = table
		self.column_name = column_name
		