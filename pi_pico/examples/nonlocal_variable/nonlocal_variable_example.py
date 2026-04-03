# nonlocal_variable.py

def outer_func():
    count = 0  # Variable in the enclosing scope
    
    def inner_func():
        nonlocal count  # Declares that we want to use the 'count' from outer_func
        count += 1
        return count
        
    return inner_func

counter = outer_func()
print(counter())  # Output: 1
print(counter())  # Output: 2
