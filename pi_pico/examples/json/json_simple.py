import json

python_dict = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "is_active": True,
    "hobbies": ["reading", "gaming", "hiking"]
}
json_string = json.dumps(python_dict)

# Print repr - same as str but has quotes around it
print(repr(json_string))
# output:
#  '{"age": 30, "hobbies": ["reading", "gaming", "hiking"], "name": "Alice", "city": "New York", "is_active": true}'

print(str(json_string))
# output:
#  {"age": 30, "hobbies": ["reading", "gaming", "hiking"], "name": "Alice", "city": "New York", "is_active": true}
 
###pretty_json_string = json.dumps(python_dict, indent=4, sort_keys=True) micropython does not support
# default separators: (', ', ': ')  - includes whitespace
pretty_json_string = json.dumps(python_dict)
print(pretty_json_string)
# Output:
#  {"age": 30, "hobbies": ["reading", "gaming", "hiking"], "name": "Alice", "city": "New York", "is_active": true}

# compact form - eliminate whitespace
pretty_json_string = json.dumps(python_dict, separators=(',', ':'))
print(pretty_json_string)
#  {"age":30,"hobbies":["reading","gaming","hiking"],"name":"Alice","city":"New York","is_active":true}