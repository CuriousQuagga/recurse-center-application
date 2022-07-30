# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 00:02:38 2021

@author: Benazeer
"""
from collections import defaultdict, namedtuple, Counter

from math import inf, sqrt
Point = namedtuple('Point', ['x', 'y'])
import datetime
now = datetime.datetime.now

import operator

class Node:
    def __init__(self, r, c, cost, distance, prev):
        self.r = r
        self.c = c
        self.cost = cost
        self.distance = distance
        self.prev = prev
        self.address = (r,c)
        self.visited = False
    def __lt__(self, other):
        return self.distance < other.distance
    def __repr__(self):
        if self.prev is not None:
            haspointer = True
        else:
            haspointer = False
        return "Node at ({},{}): {}, {}, Has pointer: {}".format(self.r, self.c, self.cost, self.distance, haspointer)
class Graph:
    def __init__(self, rows, cols, Q):
        self.graph = []
        self.rowcap = rows-1
        self.colcap = cols-1
        for r in range(rows):
            self.graph.append([None]*cols)
        for node in Q:
            self.graph[node.r][node.c] = node
#        self.connect_neighbors( Q)
        self.source = self.graph[0][0]
        self.target = self.graph[self.rowcap][self.colcap]
        self.flattened_nodes = Q.copy()
    def update_graph(self, r,c, newn):
        old = self.graph[r][c]
        self.graph[r][c] = newn
        if old==self.target:
            self.target = newn
    def get_neighbors(self, node):
        neighbors = []
        for (r,c) in [(node.r, node.c-1),
                          (node.r, node.c+1),
                          (node.r-1, node.c),
                          (node.r+1, node.c)]:
            if r<0 or c<0 or r>self.rowcap or c> self.colcap:
                continue
            neighbors.append(self.graph[r][c])
        return neighbors
def quadratic(a,b,c):
    det = sqrt(b**2 - (4*a*c))
    n1 = (-b + det)/(2*a)
    n2 = (-b - det)/(2*a)
    return(n1, n2)
          
with open("C:/Users/Benaz/Documents/Advent of Code 2021/input.txt") as f:
    start = now()
    lines = f.readlines()
    modelnumber = [9]*14
    registers = defaultdict(int)
    operations = {"add": operator.add, 
                  "mul": operator.mul,
                  "div": operator.floordiv,
                  "mod": operator.mod,
                  "eql": operator.eq}
    def run_program(modelnumber, program, registers):
        for line in program:
            parts = line.split()
            assert(len(parts) in [2,3])
            oper = parts[0]
            assert(oper in ["inp", "mul", "div", "add", "mod", "eql"])
            arg0 = parts[1]
            if len(parts)==3:
                arg1 = parts[2]
        
            if oper=="inp":
                registers[arg0] = int(modelnumber.pop())
            else:
                my_op = operations[oper]
                if arg1 not in "wxyz":
                
                    tmpreg = my_op(registers[arg0] , int(arg1))
                else:
                    tmpreg = my_op(registers[arg0], registers[arg1])
                registers[arg0] = int(tmpreg)
        
        return registers["z"]
    for mnum in range(99999999999999, 11111111111110, -1):
        registers = defaultdict(int)
        modelnumber = str(mnum)
        if "0" in modelnumber:
            continue
        modelnumber = list(modelnumber)
        modelnumber.reverse()
        result = run_program(modelnumber, lines, registers) 
        print(mnum, registers)
        if result==0:
            break
    print(mnum)
    
    print("Total time: {}".format((now()-start)))
