import sys
import inspect
sys.path.append('/home/parallels/Desktop/gem5/configs')
import m5.objects
from m5.objects import *
from m5.params import *
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

            port_dict = {}
            for port_name, port in obj_list._sub_classes[sub_obj_name]._ports.items():
                port_attr = {}
                port_attr["Description"] = port.desc
                port_attr["Name"] = port_name
                port_attr["Value"] = port
                port_attr["Type"] = Port
                port_dict[port_name] = port_attr

            param_dict = {}  # Go through each parameter item for derived class
            for pname, param in obj_list._sub_classes[sub_obj_name]._params.items():
                param_attr = {}
                param_attr["Description"] = param.desc
                param_attr["Type"] = param.ptype
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
            sub_objs[sub_obj_name] = {}
            sub_objs[sub_obj_name]['params'] = param_dict
            sub_objs[sub_obj_name]['ports'] = port_dict
        obj_tree[base_obj] = sub_objs
    # Root has a default value for eventq_indexthat referecnes a Parent which
    #   does not fit with our logic. So we set it to the default value if you
    #   call the root constructor, which is 0.
    obj_tree['SimObject']['Root']['params']['eventq_index']['Default'] = 0
    obj_tree['SimObject']['Root']['params']['eventq_index']['Value'] = 0
    return obj_tree, instance_tree

def traverse_hierarchy_root(sym_catalog, symroot):
    root = symroot.SimObject()
    name , m5_children, simroot = traverse_hierarchy(sym_catalog, symroot, root)
    name, simroot = set_ports(sym_catalog, symroot, simroot, m5_children)
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

def set_ports(sym_catalog, symobject, simobject, m5_children):

    for ports, port_info in symobject.ports.items():
        if isinstance(port_info["Value"], unicode):
            if issubclass(port_info["Type"], SimObject):
                for obj in m5_children:
                    sym, sim = obj
                    if sym == port_info["Value"]:
                        #setattr(simobject, sym, None)
                        values = sym.split(".")
                        value_to_get = getattr(simobject._parent, values[0]) #get the parent object to get the object to connect
                        port_to_get = getattr(value_to_get, values[1]) #get the actual port to connect
                        setattr(simobject, port, port_to_get)
                        break
            else:
                setattr(simobject, port, str(port_info["Value"]))
        else:
            if param_info["Value"] == port_info["Default"]:
                setattr(simobject, port, port_info["Value"])
            else:
                if str(port_info["Value"]) in symobject.connected_objects:
                    print("object exists and can be parameterized")
    for child in symobject.connected_objects:
        set_ports(sym_catalog, sym_catalog[child], getattr(simobject, child), m5_children)

    return symobject.name, simobject


def instantiate(root):
    m5.instantiate()
    m5.simulate()
