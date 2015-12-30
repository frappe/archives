import unittest, sys

sys.path.append('controllers')
sys.path.append('lib')

from wn.tests.test_files import *
from wn.tests.test_model import *
from wn.tests.test_mysql import *
from wn.tests.test_mysql_obj import *
from wn.tests.test_install import *
from wn.tests.test_permissions import *

if __name__=='__main__':
	unittest.main()