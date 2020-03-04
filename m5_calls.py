import sys
import inspect
sys.path.append('/home/parallels/Desktop/gem5/configs')
import m5.objects
from m5.objects import *
from common import ObjectList

"""
This file should contain functions that interact directly with gem5
"""

def get_obj_lists():
    """ Given a set of predertimened base classes, create a dcitionary tree
        with mappings of base classes to derived classes to parameters"""
    obj_tree = {}
    instance_tree = {}
    set_type_conv = {}
    #TODO this list is predetermined, must compile final list of all objects
    #test_objects = ['BaseXBar', 'BranchPredictor', 'BaseCPU', 'BasePrefetcher',
    #   'IndirectPredictor', 'BaseCache', 'DRAMCtrl', 'Root', 'SimpleObject',
    #  'HelloObject', 'GoodbyeObject', 'System', 'SimpleMemory', 'SimObject']
    test_objects = ['SimObject']
    sim_obj_type = getattr(m5.objects, 'SimObject', None)

    for base_obj in test_objects:
        # Create ObjectLists for each base element

        obj_list = ObjectList.ObjectList(getattr(m5.objects, base_obj, None))

        sub_objs = {}  # Go through each derived class in the Object List
        for sub_obj_name, sub_obj_val  in obj_list._sub_classes.items():
            instance_tree[sub_obj_name] = sub_obj_val

            param_dict = {}  # Go through each parameter item for derived class
            for pname, param in obj_list._sub_classes[sub_obj_name]._params.items():
                param_attr = {}
                param_attr["Description"] = param.desc
                param_attr["Type"] = param.ptype_str
                if param.ptype_str not in set_type_conv:
                    set_type_conv[param.ptype_str] = []
                if hasattr(param, 'default'):
                    if type(param.default) not in set_type_conv[param.ptype_str]:
                        set_type_conv[param.ptype_str].append(type(param.default))
                    param_attr["Default"] = param.default
                    param_attr["Value"] = param.default
                else:
                    param_attr["Default"] = None
                    param_attr["Value"] = None
                param_dict[pname] = param_attr
            sub_objs[sub_obj_name] = param_dict
        obj_tree[base_obj] = sub_objs
    # print(obj_tree['SimObject']["System"])
    return obj_tree, instance_tree

def traverse_hierarchy(sym_catalog, symobject):
    m5_children = []
    print(symobject.parameters)
    print(symobject.connected_objects)
    for child in symobject.connected_objects:
        m5_children.append(traverse_hierarchy(sym_catalog, sym_catalog[child]))
    print(symobject.name)
    instantiated = symobject.SimObject()
    if symobject.component_name == 'SrcClockDomain':
        getattr(instantiated, 'voltage_domain', VoltageDomain())
        setattr(instantiated, 'clock', '1GHz')
    for m_child in m5_children:
        print(m_child)
        setattr(instantiated, m_child[0], m_child[1])
    return (symobject.name, instantiated)

def instamtiate(root):
    root.full_system = True
    m5.instantiate()
