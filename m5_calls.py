import sys
import inspect
sys.path.append('/home/parallels/Documents/gem5/configs')
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

            port_dict = {}
            for pname, port in obj_list._sub_classes[sub_obj_name]._ports.items():
                port_attr = {}
                port_attr["Description"] = port.desc
                port_attr["Name"] = pname
                port_attr["Value"] = port
                port_attr["Type"] = Port

                port_dict[pname] = port_attr

            param_dict = {}  # Go through each parameter item for derived class
            for pname, param in obj_list._sub_classes[sub_obj_name]._params.items():
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
            sub_objs[sub_obj_name] = {}
            sub_objs[sub_obj_name]['params'] = param_dict
            sub_objs[sub_obj_name]['ports'] = port_dict
        obj_tree[base_obj] = sub_objs
    return obj_tree

def traverse_hierarchy_root(sym_catalog, symroot):
    root = symroot.SimObject()
    _ , m5_children , simroot = traverse_hierarchy(sym_catalog, symroot, root)
    return symroot.name, simroot

def traverse_hierarchy(sym_catalog, symobject, simobject):
    m5_children = []
    for child in symobject.connected_objects:
        sym, sim = sym_catalog[child].name, sym_catalog[child].SimObject()
        setattr(simobject, sym, sim)
        m5_children.append((sym, sim))

    for m_child in m5_children:
        _ , _ , _ = traverse_hierarchy(sym_catalog, sym_catalog[m_child[0]], m_child[1])

    for param, param_info in symobject.parameters.items():
        if isinstance(param_info["Value"], unicode):
            if issubclass(param_info["Type"], SimObject):
                for obj in m5_children:
                    sym, sim = obj
                    if sym == param_info["Value"]:
                        # setattr(simobject, sym, None)
                        setattr(simobject, param, sim)
                        break
            else:
                setattr(simobject, param, str(param_info["Value"]))
        else:
            if param_info["Value"] == param_info["Default"]:
                setattr(simobject, param, param_info["Value"])
            else:
                if str(param_info["Value"]) in symobject.connected_objects:
                    print("object exists and can be parameterized")




    return (symobject.name, m5_children, simobject)

def set_params(sym_catalog, symobject, simobject, m5_children):
    for param, param_info in symobject.parameters.items():
        if isinstance(param_info["Value"], unicode):
            if issubclass(param_info["Type"], SimObject):
                for obj in m5_children:
                    sym, sim = obj
                    if sym == param_info["Value"]:
                        # setattr(simobject, sym, None)
                        setattr(simobject, param, sim)
                        break
            else:
                setattr(simobject, param, str(param_info["Value"]))
        else:
            if param_info["Value"] == param_info["Default"]:
                setattr(simobject, param, param_info["Value"])
            else:
                if str(param_info["Value"]) in symobject.connected_objects:
                    print("object exists and can be parameterized")
        print(getattr(simobject, param), param)

    for child in symobject.connected_objects:
        set_params(sym_catalog, sym_catalog[child], getattr(simobject, child), m5_children)

    return symobject.name, simobject


def instantiate(root):
    m5.instantiate()
