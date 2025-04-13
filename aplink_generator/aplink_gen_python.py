# Move this into seperate repo
# FINISH THIS TODAY
# Still write parse_byte functions manually

import json
from jinja2 import Template

template = Template("""
import struct

{% for i in range(messages|length) %}        
class aplink_{{ messages[i].msg_name }}:
    format = "{{ formats[i] }}"
    msg_id = {{ messages[i].msg_id }}  
                      
    {% for field in messages[i].fields %}
    {{ field.name }} = None
    {% endfor %}
    
    def unpack(self, bytes):
        data = struct.unpack(format, bytes)
        {% for j in range(messages[i].fields|length) %}
        self.{{ messages[i].fields[j].name }} = data[{{ j }}]
        {% endfor %}
    
    def pack(self):
        return struct.pack(format{% for field in messages[i]['fields'] %}, self.{{ field['name'] }}{% endfor %})
{% endfor %}
""")

type_mappings = {
    "float": "f",
    "uint8_t": "B",
    "int8_t": "b",
    "uint16_t": "H",
    "int16_t": "h",
    "uint32_t": "I",
    "int32_t": "i",
    "double": "d",
}

messages = json.load(open("aplink_generator/messages.json", "r"))

formats = []
for message in messages:
    formats.append("".join(type_mappings[field["type"]] for field in message["fields"]))

python_code = template.render(messages=messages, formats=formats)

f = open("aplink_generator/output/aplink_py/aplink.py", "w")
f.write(python_code)
f.close()