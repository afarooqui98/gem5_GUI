import m5
from m5 import SimObject
from ObjectList import ObjectList
import json
from ObjectList import ObjectList



obj_tree = {}

test_objects = ['BaseXBar', 'BranchPredictor', 'BaseCPU', 'BasePrefetcher', 'IndirectPredictor', 'BaseCache', 'DRAMCtrl', 'Root', 'SimpleObject', 'HelloObject', 'GoodbyeObject']


for i in range(len(test_objects)):
    name = test_objects[i]
    obj_list = ObjectList(getattr(m5.objects, name, None))
    sub_objs = {}
    for sub_obj in obj_list._sub_classes.keys():
        param_dict = {}
        for pname, param in obj_list._sub_classes[sub_obj]._params.items():
            param_attr = {}
            param_attr["Description"] = param.desc
            param_attr["Type"] = param.ptype_str
            if hasattr(param, 'default'):

                # TODO Must convert default to string for object values
                #  in order to dump to json. Need way to access object?
                param_attr["Default"] = str(param.default)
                param_attr["Value"] = str(param.default)
            else:
                param_attr["Default"] = None
                param_attr["Value"] = None
            param_dict[pname] = param_attr
        sub_objs[sub_obj] = param_dict

    obj_tree[name] = sub_objs


with open('result.json', 'w') as fp:
    json.dump(obj_tree, fp)
