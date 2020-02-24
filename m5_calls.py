import sys
sys.path.append('configs')
import m5.objects
from common import ObjectList

"""
This file should contain functions that interact directly with gem5
"""

def get_obj_lists():
    """ Given a set of predertimened base classes, create a dcitionary tree
        with mappings of base classes to derived classes to parameters"""
    obj_tree = {}

    #TODO this list is predetermined, must compile final list of all objects
    test_objects = ['BaseXBar', 'BranchPredictor', 'BaseCPU', 'BasePrefetcher',
        'IndirectPredictor', 'BaseCache', 'DRAMCtrl', 'Root', 'SimpleObject',
        'HelloObject', 'GoodbyeObject']

    for i in range(len(test_objects)):
        # Create ObjectLists for each base element
        name = test_objects[i]
        obj_list = ObjectList.ObjectList(getattr(m5.objects, name, None))

        sub_objs = {}  # Go through each derived class in the Object List
        for sub_obj in obj_list._sub_classes.keys():

            param_dict = {}  # Go through each parameter item for derived class
            for pname, param in obj_list._sub_classes[sub_obj]._params.items():
                param_attr = {}
                param_attr["Description"] = param.desc
                param_attr["Type"] = param.ptype_str
                if hasattr(param, 'default'):

                    param_attr["Default"] = str(param.default)
                    param_attr["Value"] = str(param.default)
                else:
                    param_attr["Default"] = None
                    param_attr["Value"] = None
                param_dict[pname] = param_attr
            sub_objs[sub_obj] = param_dict

        obj_tree[name] = sub_objs
