import sys
import os
import inspect
from gui_views.state import *
get_path()
sys.path.append(os.getenv('gem5_path'))
import m5.objects
from m5.objects import *
from m5.params import *
from m5.proxy import AttrProxy
from common import ObjectList

"""
This file should contain functions that interact directly with gem5
"""

def get_obj_lists():
    """ Given a set of predertimened base classes, create a dcitionary tree
        with mappings of base classes to derived classes to parameters"""
    obj_tree = {}
    instance_tree = {}
    set_subtypes = set()
    #TODO this list is predetermined, must compile final list of all objects
    categories = ['BaseXBar', 'BranchPredictor', 'BaseCPU', 'BasePrefetcher',
       'IndirectPredictor', 'BaseCache', 'DRAMCtrl', 'Root', 'BaseInterrupts',
         'SimObject']
    sim_obj_type = getattr(m5.objects, 'SimObject', None)

    for base_obj in categories:
        # Create ObjectLists for each base element

        obj_list = ObjectList.ObjectList(getattr(m5.objects, base_obj, None))
        set_subtypes.add(base_obj)
        sub_objs = {}  # Go through each derived class in the Object List
        for sub_obj_name, sub_obj_val  in obj_list._sub_classes.items():
            if base_obj == 'SimObject':
                if sub_obj_name in set_subtypes:
                    continue
            else:
                set_subtypes.add(sub_obj_name)

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
                if hasattr(param, 'default'):
                    param_attr["Default"] = param.default
                    param_attr["Value"] = param.default
                else:
                    param_attr["Default"] = None
                    param_attr["Value"] = None
                param_dict[pname] = param_attr
            sub_objs[sub_obj_name] = {}
            sub_objs[sub_obj_name]['params'] = param_dict
            sub_objs[sub_obj_name]['ports'] = port_dict
        if base_obj == 'SimObject':
            base_obj = 'Other'
        obj_tree[base_obj] = sub_objs
    # Root has a default value for eventq_indexthat referecnes a Parent which
    #   does not fit with our logic. So we set it to the default value if you
    #   call the root constructor, which is 0.
    obj_tree['Root']['Root']['params']['eventq_index']['Default'] = 0
    obj_tree['Root']['Root']['params']['eventq_index']['Value'] = 0
    return obj_tree, instance_tree

#eager instantiation occurs here, pass through object from state via current_sym_object
def instantiate_object(object):
    param_dict = object.SimObject.enumerateParams()

    print(object.name)
    print(object.parameters)
    print(param_dict)
    print()

    for param, value in object.parameters.items():
        if(isinstance(object.parameters[param]["Default"], AttrProxy)):
            print("encountered proxy parameters")
            continue #want to skip proxy parameters, want to do this lazily

        if param_dict.get(param) == None:
            # Some parameters are included in the class but not in the actual
            #   parameters given in enumerateParams TODO: look into this
            continue
        else:
            #the objects param_dictionary is replaced from the preloaded
            #"catalog" values to the instantiated value
            # if hasattr(param_dict[param], 'default'):
            #     object.parameters[param]["Default"] = param_dict[param].default
            #     object.parameters[param]["Value"] = param_dict[param].default


            if param_dict[param].default_val != "":
                object.parameters[param]["Default"] = param_dict[param].default_val
                object.parameters[param]["Value"] = param_dict[param].default_val
            else:
                continue

#instantiation occurs here when an object is loaded from a model file
def load_instantiate(object):
    object.SimObject = object.SimObject()
    param_dict = object.SimObject._params

    print(object.name)
    print(object.parameters)
    print(param_dict)

    # Some parameters are included in the class but not in the actual parameters
    #   given in enumerateParams TODO: look into this
    weird_params = []

    #TODO: handle proxy params here!!!!
    for param, param_info in object.parameters.items():
        if param_dict.get(param) == None:
            weird_params.append(param)
            continue

        #Check is set since some of the types for parametrs are VectorParam objs
        if inspect.isclass(param_dict[param].ptype):
            object.parameters[param]["Type"] = param_dict[param].ptype
        else:
            object.parameters[param]["Type"] = type(param_dict[param].ptype)

        object.parameters[param]["Description"] = param_dict[param].desc

        if hasattr(param_dict[param], 'default'):
            object.parameters[param]["Default"] = param_dict[param].default
        else:
            object.parameters[param]["Default"] = None

        #If the value was changed in the model file then no need to load in
        #   the default, otherwise the value is set to the default
        if "Value" not in object.parameters[param]:
            object.parameters[param]["Value"] = \
                object.parameters[param]["Default"]

    for i in range(len(weird_params)):
        del object.parameters[weird_params[i]]

    instantiate_object(object) #enumerate over params to assign default values

    if object.component_name == "Root":
        print(object.parameters)
        object.state.mainWindow.buttonView.exportButton.setEnabled(True)

#recursively set parameters (ONLY if changed?) and then recursively set ports
def traverse_hierarchy_root(sym_catalog, symroot):
    root = symroot.SimObject
    name , m5_children, simroot = traverse_hierarchy(sym_catalog, symroot, root)
    name, simroot = set_ports(sym_catalog, symroot, simroot, m5_children)
    return symroot.name, simroot


def traverse_hierarchy(sym_catalog, symobject, simobject):
    m5_children = []

    for child in symobject.connected_objects:
        sym, sim = sym_catalog[child].name, sym_catalog[child].SimObject
        setattr(simobject, sym, sim)
        m5_children.append((sym, sim))

    #TODO: possible error with the eager instantiation happening here?
    #set user-defined attributes here, do some type checking to do different things
    for param, param_info in symobject.parameters.items():
        if isinstance(param_info["Value"], unicode):
            print(param_info["Type"])
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
            if param_info["Value"] == param_info["Default"]: #
                if isinstance(param_info["Default"], AttrProxy):
                    result, found = param_info["Default"].find(simobject)
                    if not found:
                        print("PROXY GOING BAD")
                    else:
                        print("simobject is " + str(simobject))
                        print("param is " + str(param_info["Default"]))
                        param_info["Value"] = result
                setattr(simobject, param, param_info["Value"])
            else:
                if str(param_info["Value"]) in symobject.connected_objects:
                    print("object exists and can be parameterized")

    for m_child in m5_children:
        _ , _ , _ = traverse_hierarchy(sym_catalog, sym_catalog[m_child[0]], m_child[1])

    return (symobject.name, m5_children, simobject)

#port setting for objects
def set_ports(sym_catalog, symobject, simobject, m5_children):

    for ports, port_info in symobject.ports.items():
        if isinstance(simobject, list): #for vector param value
            print("we have a vector!")
            for i in range(len(simobject)):
                if isinstance(port_info["Value"], str):
                    values = port_info["Value"].split(".")
                    print(sym_catalog[values[0]].SimObject)
                    print(getattr(sym_catalog[values[0]].SimObject, values[1]))
                    setattr(simobject[i], ports, getattr(sym_catalog[values[0]].SimObject, values[1]))
                    print("simobject is: " + str(simobject[i]) + " ports are: " + str(ports))
                    print(getattr(simobject[i], ports))
                    print(port_info)
                    print(values)
                    print(getattr(simobject[i], ports).ini_str())
                # else:
                #         setattr(simobject, port, str(port_info["Value"]))
                else:
                    print("GOING BAD")
                    # if param_info["Value"] == port_info["Default"]:
                    #     setattr(simobject, port, port_info["Value"])
                    # else:
                    #     if str(port_info["Value"]) in symobject.connected_objects:
                    #         print("object exists and can be parameterized")
        else:
            if isinstance(port_info["Value"], str): #nonvector param value
                values = port_info["Value"].split(".")
                print(sym_catalog[values[0]].SimObject)
                print(getattr(sym_catalog[values[0]].SimObject, values[1]))
                setattr(simobject, ports, getattr(sym_catalog[values[0]].SimObject, values[1]))
                print("simobject is: " + str(simobject) + " ports are: " + str(ports))
                print(getattr(simobject, ports))
                print(port_info)
                print(values)
                print(getattr(simobject, ports).ini_str())
                # value_to_get = getattr(simobject._parent, values[0]) #get the parent object to get the object to connect
                # port_to_get = getattr(value_to_get, values[1]) #get the actual port to connect
                # setattr(simobject, port, port_to_get)
            # else:
            #         setattr(simobject, port, str(port_info["Value"]))
            else:
                print("GOING BAD")
                # if param_info["Value"] == port_info["Default"]:
                #     setattr(simobject, port, port_info["Value"])
                # else:
                #     if str(port_info["Value"]) in symobject.connected_objects:
                #         print("object exists and can be parameterized")
    for child in symobject.connected_objects:
        set_ports(sym_catalog, sym_catalog[child], getattr(simobject, child), m5_children)

    return symobject.name, simobject

def object_instantiate(object):
    object.SimObject = object.SimObject()
    instantiate_object(object)

def instantiate():
    m5.instantiate()

def simulate():
    exit_event = m5.simulate()
    print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
