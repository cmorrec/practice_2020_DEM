from math import *

radius = 1

for i in range(0,24):
    print(radius * (1 + sin(i*pi/12)), radius * (1 - cos(i*pi/12)))