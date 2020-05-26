import sys
import os
import unittest
from gui_views.state import get_path

get_path()
sys.path.append(os.getenv('gem5_path'))

from m5_calls import *

class M5CallTester():
    def __init__(self):
        self.catalog = None

    def catalogTest(self):
        new_catalog = get_obj_lists()
        if new_catalog != None:
            self.catalog = new_catalog
            return True
        else:
            return False

    def objectTest(self, object):
        return isSimObject(object)

    def portTest(self, object):
        port_info = getPortInfo(object)
        if port_info is None:
            return False
        if (len(port_info) != len(object._ports)):
            print(object)
            print([key for key in port_info.keys()])
            print([cey for cey in object._ports.keys()])
        return (len(port_info) == len(object._ports))

    def paramTest(self, object):
        param_info = getParamInfo(object)
        if param_info is None:
            return False
        if (len(param_info) != len(object._params)):
            print(object)
            print([key for key in param_info.keys()])
            print([cey for cey in object._params.keys()])
        return (len(param_info) == len(object._params))

    def setParamValueTest(self, object):
        param_info = getParamInfo(object)
        for key1, key2 in zip(param_info.keys(), object._params.keys()):
            if type(key1) != type(key2):
                print("type mismatch found")
                return False
        return True

    def setPortValueTest(self, object):
        port_info = getPortInfo(object)
        for key1, key2 in zip(port_info.keys(), object._ports.keys()):
            if type(key1) != type(key2):
                print("port type mismatch found")
                return False
        return True

tester = M5CallTester()
print(tester.catalogTest())
for key, value in tester.catalog[1].items():
    if not tester.objectTest(value):
        print(value)
    if tester.portTest(value):
        tester.setPortValueTest(value)
    else:
        print("Port")
        print(value)
    if tester.paramTest(value):
        tester.setParamValueTest(value)
    else:
        print("Param")
        print(value)
