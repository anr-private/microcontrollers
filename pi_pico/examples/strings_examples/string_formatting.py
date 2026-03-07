# string formatting examples

# Not supported:
#   from string import Template

# format_map is not supported in micropython
def use_format_map():
    template = "This is a template {name} is a {occupation}"
    data = {"name": "Bob", "occupation": "plumber"}
    s = template.format_map(data)
    print(f" data is {data}")
    print(f" formatted string: '{s}'")
    
def use_format():
    print("\n=== FORMAT(**data)    ===================")
    template = "This is a template {name} is a {occupation}"
    data = {"name": "Bob", "occupation": "plumber"}
    s = template.format(**data)
    print(f" data is {data}")
    print(f" formatted string: '{s}'")
    
def use_f_string():
    print("\n=== F-STRING     ===================")
    data = {"name": "Bob", "occupation": "plumber"}
    s = f"This is a template {data.get('name')} is a {data['occupation']}"
    print(f" data is {data}")
    print(f" formatted string: '{s}'")
    
    
def main():
    use_format()
    use_f_string()
   
   
if  __name__ == "__main__":
    main()
    
###