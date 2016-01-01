# Copyright (c) 2013, Web Notes Technologies and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

test_records = frappe.get_test_records('Registrant')

class TestRegistrant(unittest.TestCase):
	pass
