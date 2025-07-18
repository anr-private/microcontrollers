import time
from random import random

for i in range(100):
    y1 = random() * 10
    y2 = random() * 5 + 5 # second y value
    ###print(f"x: {x}, y1: {y1}, y2: {y2}")
    print(f"i: {i}, y1: {y1}, y2: {y2}")
    time.sleep(0.1)


### end ###
