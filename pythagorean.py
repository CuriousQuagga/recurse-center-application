# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:09:44 2021

@author: Benazeer
"""
from euler_utils import *
import math
import fractions
# a^2 + b^2 = c^2
# a + b + c = P
# a + b + sqrt(a^2 + b^2) = P
# sqrt(a^2 + b^2) = P - D
# where D = a + b
# a^2 + b^2 = (P - D)^2
# a^2 + b^2 = P^2 - 2PD + D^2
# a^2 + b^2 = P^2 - 2P(a+b) + a^2 + 2ab + b^2
# 0 =  P*2 - 2Pa - 2Pb + 2ab
# 2Pa - P^2 = 2ab - 2Pb
# (2Pa - P^2)/(2a - 2P) = b


def get_b(a, P):
    return (2*P*a - P**2)/(2*a - 2*P)

# solutions = {}
# sqrt2 = math.sqrt(2)
# for P in range(12,1500001):
#     # no need to sweep a past the length of a leg
#     # for a 45-45-90 triangle
#     # a = b
#     # a^2 + b^2 = c^2
#     # a^2 + a^2 = c^2
#     # c = sqrt(2a^2) = a * sqrt(2)
#     # P = a + a + a * sqrt(2)
#     #   = a * (2 + sqrt(2))
#     sols  =0
#     for a in range(1, int(P/(2+sqrt2))+1):
#         b = get_b(a,P)
#         if b == int(b):
#             c = P - a - int(b)
#             if a**2 + b**2==c**2:
#                 sols +=1
#     solutions[P] = sols

# a=m^{2}-n^{2},\ \,b=2mn,\ \,c=m^{2}+n^{2}
# for arbitrary m, n, m> n> 0
# triple is primitive if m,n coprime and not both odd
# P = a + b + c
#   = m^2 - n^2 + 2mn + m^2 + n^2
#   = 2m^2 + 2mn
# sols = [0]*1500001
# for m in range(2,1500001):

#     for n in range((m%2)+1, m,2):
#         if get_gcd(m,n) > 1:
#             continue
#         P = 2*m**2 + 2*m*n
#         if P >1500000:
#             break
#         for k in range(P, 1500001, P):
#             sols[k] +=1
# print(len([x for x in sols if x==1]))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x==other.x and self.y==other.y
    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.distance_from(Point(0,0)) < other.distance_from(Point(0,0))
    def __hash__(self):
        return hash((self.x, self.y))
    def __repr__(self):
        return "({} , {})".format(self.x, self.y)
    
    def distance_from(self, p2):
        rise = abs(self.y - p2.y)
        run = abs(self.x - p2.x)
        return math.sqrt(rise**2 + run**2)
    def slope_from(self,p2):
        rise = self.y - p2.y
        run = self.x- p2.x
        if run==0:
            return math.inf
        return fractions.Fraction(rise,run)
    



lmt = 50
# for every point on the y axis, we can construct 3N triangles with 
# with horizontal and vertical legs
count = lmt*(lmt*3)
testrights = []

for x in range(1, lmt+1):
    for y in range(x, lmt+1):
    # no need to test m's value -- we've guaranteed it is neither 
    # inf or 0 by excluding 0 from the ranges used to construct the 
    # list of points
        #find all points on the line through pt1 with slope -1/m
        # y = m'x+b -> b = y - m'x
        # m' = -1/m -- > b =y + x/m
        # 
        g = get_gcd(x,y)
        rise = int(-x/g)
        run = int(y/g)
        x2 = x - run
        y2 = y - rise
        
        while x2 >=0 and y2 >= 0 and x2 <= lmt and y2<=lmt:
            count +=2
            x2 = x2 - run
            y2 = y2 -rise
        if x==y:
            continue
        x2 = x + run
        y2 = y + rise
        while x2 >=0 and y2 >= 0 and x2 <= lmt and y2<=lmt:
            count +=2
            x2 = x2 +  run
            y2 = y2 + rise
           
    
print(count)
         