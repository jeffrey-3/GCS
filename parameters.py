import json
import struct

def flatten_array(arr):
    flattened = []
    
    def recursive_flatten(element):
        if isinstance(element, list):
            for item in element:
                recursive_flatten(item)
        else:
            flattened.append(element)
    
    recursive_flatten(arr)
    return flattened

file = open("parameters/flightgear_yardstik.json", "r")
data = json.load(file)
format = data['format']
params = data['params']

values = []
for key in params:
    values.extend(flatten_array(params[key]))

print(values)
print(struct.pack(format, *values))
print(struct.calcsize(format))