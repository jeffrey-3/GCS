from app.utils.data_structures import *
from app.utils.utils import *
import json

class ParamsModel:
    def __init__(self):
        self.params_values = None
        self.params_format = None

    def process_params_file(self, path):
        file = open(path, "r")
        data = json.load(file)
        self.params_format = data['format']
        params = data['params']
        self.params_values = []
        for key in params:
            self.params_values.extend(flatten_array(params[key]))