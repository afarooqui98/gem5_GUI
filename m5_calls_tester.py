import sys
import os
import unittest
from gui_views.state import get_path

get_path()
sys.path.append(os.getenv('gem5_path'))
class M5CallTester():
    def __init__(self):
        self.catalog = None

    def catalogTest(self):
        from m5_calls import get_obj_lists
        new_catalog = get_obj_lists()
        if new_catalog != None:
            self.catalog = new_catalog
            return True
        else:
            return False

    def objectTest(self, object):
        from m5_calls import isSimObject
        return isSimObject(object)

    def portTest(self, object):
        from m5_calls import getPortInfo
        return (True if getPortInfo(object) else False)


tester = M5CallTester()
print(tester.catalogTest())
for key, value in tester.catalog[1].items():
    print(tester.objectTest(value))
    print(tester.portTest(value))
