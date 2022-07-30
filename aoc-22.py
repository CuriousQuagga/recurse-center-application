# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 18:52:20 2021

@author: Benazeer
"""
from collections import defaultdict, namedtuple, Counter

from math import inf, sqrt
Point = namedtuple('Point', ['x', 'y', 'z'])
import datetime
now = datetime.datetime.now
Cube = namedtuple('Cube', ['polarity','ll', 'ur'])
import operator

def get_points(line):
    if "on" in line:
        line = line.replace("on ", "")
        polarity = 1
    elif "off" in line:
        line = line.replace("off ", "")
        polarity = 0
    else:
        raise ValueError
    parts = line.split(",")
    eps = []
    for p in parts:
        p = p.split("=")
        p = p[1]
        eps.append(p.split(".."))
    x0 = int(eps[0][0])
    x1 = int(eps[0][1]) 
    y0 = int(eps[1][0])
    y1 = int(eps[1][1]) 
    z0 = int(eps[2][0])
    z1 = int(eps[2][1]) 
    ll = Point(x0, y0, z0)
    ur = Point(x1, y1, z1)
    
    return(Cube(polarity, ll, ur))
def split_cube(c, coord, axis):
   # print("Splitting cube {} at {}={}".format(c, axis, coord))
    polarity = c.polarity
    ll = c.ll
    ur = c.ur
    if axis=="x" and ll.x==ur.x:
        return None
    elif axis=="y" and ll.y==ur.y:
        return None
    elif axis=="z" and ll.z==ur.z:
        return None
    elif axis=="x" and coord > ll.x and coord <=ur.x:
        ll1 = ll
        ur1 = Point(coord-1, ur.y, ur.z)
        ll2 = Point(coord, ll.y, ll.z)
        ur2 = ur
    elif axis=="x" and coord==ll.x:
        ll1 = ll
        ur1 = Point(coord, ur.y, ur.z)
        ll2 = Point(coord+1, ll.y, ll.z)
        ur2 = ur
    elif axis=="y" and coord > ll.y and coord <=ur.y:
        ll1 = ll
        ur1 = Point(ur.x, coord-1, ur.z)
        ll2 = Point(ll.x, coord, ll.z)
        ur2 = ur
    elif axis=="y" and coord==ll.y:
        ll1 = ll
        ur1 = Point(ur.x, coord, ur.z)
        ll2 = Point(ll.x, coord+1, ll.z)
        ur2 = ur
    elif axis=="z" and coord > ll.z and coord <=ur.z:
        ll1 = ll
        ur1 = Point(ur.x, ur.y, coord-1)
        ll2 = Point(ll.x, ll.y, coord)
        ur2 = ur
    elif axis=="z" and coord == ll.z :
        ll1 = ll
        ur1 = Point(ur.x, ur.y, coord)
        ll2 = Point(ll.x, ll.y, coord+1)
        ur2 = ur
    else:
        return None
    return (Cube(polarity, ll1, ur1), Cube(polarity, ll2, ur2))


def get_area(c):
    ll = c.ll
    ur = c.ur
    dx = abs(ur.x + 1 - ll.x)
    dy = abs(ur.y +1 - ll.y)
    dz = abs(ur.z +1 - ll.z)
    return dx * dy * dz
def cube_to_points(c):
    ll = c.ll
    ur = c.ur
    for x in range(ll.x, ur.x+1):
        for y in range(ll.y, ur.y+1):
            for z in range(ll.z, ur.z+1):
                yield (Point(x,y,z))
            
                
def dumb_impl(lines):
    onpoints = {}
    for line in lines:
        if "on" in line:
            for p in cube_to_points(*get_points(line)):
                onpoints[p] = True
        elif "off" in line:
            for p in cube_to_points(*get_points(line)):
                onpoints.pop(p,None)
    
    print(len(onpoints))
def cube_intersect(c0, c1):
    cubes = [c0, c1]
    xint = False
    yint = False
    zint = False
    if c0.ll.x>c1.ll.x and c0.ll.x<c1.ur.x:
        xint = True
    elif c0.ur.x>c1.ll.x and c0.ur.x<c1.ur.x:
        xint = True
    elif c1.ll.x>c0.ll.x and c1.ll.x<c0.ur.x:
        xint = True
    elif c1.ur.x>c0.ll.x and c1.ur.x<c0.ur.x:
        xint = True
    elif c0.ur.x==c1.ll.x:
        xint = True
    elif c1.ur.x==c0.ll.x:
        xint = True
    if c0.ll.y>c1.ll.y and c0.ll.y<c1.ur.y:
        yint = True
    elif c0.ur.y>c1.ll.y and c0.ur.y<c1.ur.y:
        yint = True
    elif c1.ll.y>c0.ll.y and c1.ll.y<c0.ur.y:
        yint = True
    elif c1.ur.y>c0.ll.y and c1.ur.y<c0.ur.y:
        yint = True
    elif c0.ur.y==c1.ll.y:
        yint = True
    elif c1.ur.y==c0.ll.y:
        yint = True
    if c0.ll.z>c1.ll.z and c0.ll.z<c1.ur.z:
        zint = True
    elif c0.ur.z>c1.ll.z and c0.ur.z<c1.ur.z:
        zint = True
    elif c1.ll.z>c0.ll.z and c1.ll.z<c0.ur.z:
        zint = True
    elif c1.ur.z>c0.ll.z and c1.ur.z<c0.ur.z:
        zint = True
    elif c0.ur.z==c1.ll.z:
        zint = True
    elif c1.ur.z==c0.ll.z:
        zint = True
    return (xint and yint and zint  )

def combine_cubes(c0, c1):
    if not cube_intersect(c0, c1):
        if c1.polarity==1:
            return [c0, c1]
        else:
            return [c0]
    
    
            
    
    
with open("C:/Users/Benaz/Documents/Advent of Code 2021/input.txt") as f:
    start = now()
    lines = f.readlines()
    cubes = []
    for ct, line in enumerate(lines):
        cubes.append(get_points(line))
    
    union = [cubes[0]]
    for c in cubes[1:]:
        print(c, len(union))
        newunion = []
        for u in union:
            newunion.extend(combine_cubes(u, c))
        union=newunion.copy()
            
    print("total time: {}".format(now()-start))
            
    
    
    print(sum([get_area(*c) for c in union]))