import json
import struct
from utils import flatten_array

def get_param_pkt():

    file = open("examples/parameters/flightgear_yardstik.json", "r")
    data = json.load(file)
    format = data['format']
    params = data['params']

    values = []
    for key in params:
        values.extend(flatten_array(params[key]))

    print(values)
    print(struct.pack(format, *values))
    print(struct.calcsize(format))

get_param_pkt()