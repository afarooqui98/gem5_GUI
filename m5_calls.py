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
    """ Given a set of predertimened base classes creates two dictionaries used
        for metadata purposes in the gui.

        The first is a nested dictionary which maps base object names to another
        dictionary which maps the sub-object name to a dictionary containing
        parameter info.

        The second dictionary maps an object's name to the actual class in
        m5.objects to be used for instantiating objects.
        """
    obj_tree = {}
    instance_tree = {}
    # set_subtypes is used to not double count objects already in the dicts
    set_subtypes = set()

    #TODO this list is predetermined, must compile final list of all objects
    categories = ['BaseXBar', 'BranchPredictor', 'BaseCPU', 'BasePrefetcher',
       'IndirectPredictor', 'BaseCache', 'DRAMCtrl', 'Root', 'BaseInterrupts',
         'SimObject']

    for base_obj in categories:
        # Create ObjectLists for each base element
        obj_list = ObjectList.ObjectList(getattr(m5.objects, base_obj, None))
        set_subtypes.add(base_obj)

        sub_objs = {}  # Go through each derived class in the Object List
        for sub_obj_name, sub_obj_inst  in obj_list._sub_classes.items():
            if base_obj == 'SimObject':
                # SimObject will have all objects as derived classes so we
                #   need to make sure we don't double count. This is why
                #   SimObject is the last element in categories
                if sub_obj_name in set_subtypes:
                    continue
            else:
                set_subtypes.add(sub_obj_name)

            instance_tree[sub_obj_name] = sub_obj_inst #Save the object instance

            port_dict = {} #Save port info for the objects
            for port_name, port in \
            obj_list._sub_classes[sub_obj_name]._ports.items():
                port_attr = {"Description": port.desc, 'Name': port_name, \
                'Value': port,  'Type': Port}

                port_dict[port_name] = port_attr

            param_dict = {}  # Go through each parameter item for derived class
            for pname, param in \
            obj_list._sub_classes[sub_obj_name]._params.items():
                param_attr = {'Description': param.desc, 'Type': param.ptype}
                if hasattr(param, 'default'):
                    param_attr["Default"] = param.default
                    param_attr["Value"] = param.default
                else:
                    param_attr["Default"] = None
                    param_attr["Value"] = None
                param_dict[pname] = param_attr

            sub_objs[sub_obj_name] = {'params': param_dict, 'ports': port_dict}

        if base_obj == 'SimObject':
            base_obj = 'Other'
        obj_tree[base_obj] = sub_objs
    # Root has a default value for eventq_indexthat referecnes a Parent which
    #   does not fit with our logic. So we set it to the default value if you
    #   call the root constructor, which is 0.
    obj_tree['Root']['Root']['params']['eventq_index']['Default'] = 0
    obj_tree['Root']['Root']['params']['eventq_index']['Value'] = 0
    return obj_tree, instance_tree


def get_param_info(object):
    """Get additional info on params such as default values  after
        instantiating object. This information is held in a dictionary produced
        from calling enumerate_params method on instantiated object """
    #calling enumerate_params to get exact values for paramaters
    param_dict = object.SimObject.enumerateParams()

    for param, value in object.parameters.items():
        if(isinstance(object.parameters[param]["Default"], AttrProxy)):
            continue #want to skip proxy parameters, want to do this lazily

        if param_dict.get(param) == None:
            # Some parameters are included in the class but not in the actual
            #   parameters given in enumerateParams TODO: look into this
            continue
        else:
            #if we load from a ui file, check if the default and value params
            # are diferent
            if object.parameters[param]["Value"] != \
                    object.parameters[param]["Default"]:
                continue

            if param_dict[param].default_val != "": #if there is a default value
                default = param_dict[param].default_val
                object.parameters[param]["Default"] = default
                object.parameters[param]["Value"] = default
            else:
                continue


#Instantiation occurs here when an object is loaded from a model file
def load_instantiate(object):
    """Instantiation and some paramter/port info collection occurs here when an
        object is loaded from a model file """
    object.SimObject = object.SimObject()
    param_dict = object.SimObject._params
    port_dict = object.SimObject._ports

    # Some parameters are included in the class but not in the actual parameters
    #   given in enumerateParams TODO: look into this!!!
    weird_params = []

    for port, port_info in object.ports.items():
        if port_info["Value"] == None:
            port_info["Value"] = port_dict.get(port) #load default port

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

    get_param_info(object) #enumerate over params to assign default values

    if object.component_name == "Root":
        # allows user to click on intantiate button
        object.state.mainWindow.buttonView.instantiate.setEnabled(True)

#r
def traverse_hierarchy_root(sym_catalog, symroot):
    """Recursively set parameters and then recursively set ports for
        instantiated objs"""
    root = symroot.SimObject
    name, simroot = traverse_hierarchy(sym_catalog, symroot, root)
    name, simroot = set_ports(sym_catalog, symroot, simroot)
    return symroot.name, simroot


def traverse_hierarchy(sym_catalog, symobject, simobject):
    """ Recursively goes through object tree starting at symobject and
    set parametersfor corresponding simobject """

    m5_children = []
    # Setting the connections for the child objects
    for child in symobject.connected_objects:
        sym, sim = sym_catalog[child].name, sym_catalog[child].SimObject
        setattr(simobject, sym, sim)
        m5_children.append((sym, sim))

    # Setting the paramerters for the object
    for param, param_info in symobject.parameters.items():
        # When a user types in a value for a param in the gui it becomes unicode
        if isinstance(param_info["Value"], unicode):
            # Check if the param's type is another Simobject, which means
            #   it must be set as a child of the object already
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
            # If the user has not changed and there is a default
            if param_info["Value"] == param_info["Default"]:
                # If the param is an AttrProxy, set it using find
                if isinstance(param_info["Default"], AttrProxy):
                    result, found = param_info["Default"].find(simobject)
                    if not found:
                        print("PROXY GOING BAD")
                    else:
                        param_info["Value"] = result
                setattr(simobject, param, param_info["Value"])
            else:
                if str(param_info["Value"]) in symobject.connected_objects:
                    print("object exists and can be parameterized")

    # Recurse for the objects children
    for m_child in m5_children:
        traverse_hierarchy(sym_catalog, sym_catalog[m_child[0]], m_child[1])

    return (symobject.name, simobject)

def connect_port(ports, port_info, sym_catalog, simobject):
    """Create a port connection between two simobjects"""
    if isinstance(port_info["Value"], str):
        values = port_info["Value"].split(".")
        #set port value, ex: values = ['system', 'system_port']
        setattr(simobject, ports, getattr(sym_catalog[values[0]].SimObject,\
                values[1]))
    else:
        pass
        #TODO figure out why its getting into else case


def set_ports(sym_catalog, symobject, simobject):
    """ Traverse object tree starting at simobject and set ports recursively """
    for ports, port_info in symobject.ports.items():
        if isinstance(simobject, list): #for vector param value
            for i in range(len(simobject)):
                connect_port(ports, port_info, sym_catalog, simobject[i])
        else:
            connect_port(ports, port_info, sym_catalog, simobject)
            #nonvector param value

    #set ports for children
    for child in symobject.connected_objects:
        set_ports(sym_catalog, sym_catalog[child], getattr(simobject, child))

    return symobject.name, simobject


def object_instantiate(object):
    """ Creates an instantiated object for the symobject and gets any new
        info on the parameters """
    object.SimObject = object.SimObject()
    get_param_info(object)

def instantiate_model():
    m5.instantiate()

def simulate():
    exit_event = m5.simulate()
    print('Exiting @ tick %i because %s' %(m5.curTick(), exit_event.getCause()))
