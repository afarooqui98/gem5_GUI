from m5 import SimObject
import json 

print("SimObjects:")
objects = list(SimObject.allClasses.keys())
objects.sort()
obj_param = {}

for name in objects:
    obj = SimObject.allClasses[name]
    print("Obj: " + name)
    param_dict = {}

    for key, val in obj._params.items():
        param_attr = {}
        print("Parameter: " + key)
        print("Description: " + val.desc)
        param_attr["Description"] = val.desc
        param_attr["Type"] = val.ptype_str
        if hasattr(val, 'default'):
            print("Default Val: " + str(val.default))

                # TODO Must convert default to string for object values
                #  in order to dump to json. Need way to access object?

            param_attr["Default"] = str(val.default)
        else:
            param_attr["Default"] = None
        param_dict[key] = param_attr
        print()
    print()
    params = list(obj._params.keys())
    params.sort()
    #print(params)
    obj_param[name] = param_dict

with open('result.json', 'w') as fp:
    json.dump(obj_param, fp)
