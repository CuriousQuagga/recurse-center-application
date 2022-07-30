# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 10:03:49 2022

@author: Benazeer
"""
import itertools
import datetime
now = datetime.datetime.now

def explode(snail):
    def look_back(loc, snail):
        for i in range(loc, -1, -1):
            if isinstance(snail[i], int):
                return i
        return None
    def look_forward(loc, snail):
        for i in range(loc, len(snail)):
            if isinstance(snail[i], int):
                return i
        return None
    counter = 0
    for idx,c in enumerate(snail):
        if c=="[":
            counter+=1
        elif c=="]":
            counter = counter -1
        if counter==5:
            left = snail[idx+1]
            right = snail[idx+2]
            lb = look_back(idx, snail)
            lf = look_forward(idx+3, snail)
            if lb is not None:
                left = left + snail[lb]
                lefthalf = snail[:lb] + [left] + snail[lb+1:idx]
            else:
                lefthalf = snail[:idx]
            if lf is not None:
                right =  right + snail[lf]
                righthalf = snail[idx+4: lf] + [right] + snail[lf+1:]
            else:
                righthalf = snail[idx+4:]
            snail = lefthalf + [0] + righthalf
            return snail
    return snail
            
def read_snailfish(line):
    snail = []
    double_digit = False
    for idx, c in enumerate(line):  
        if c in "[]":
            snail.append(c)
        elif c.isdigit() and not double_digit:
            peek = line[idx+1]
            if peek.isdigit():
                c = c + peek
                double_digit = True
            snail.append(int(c))
        elif c.isdigit() and double_digit:
            double_digit = False
    return snail                
  
def split(snail):
    for idx,c in enumerate(snail):
        if isinstance(c, int) and c>9:
            left = c//2
            right = c-left
            snail = snail[:idx] + ["[", left, right, "]"] + snail[idx+1:]
            return snail
    return snail
def reduce(sn):
    
    exploded = explode(sn)
    if exploded != sn:
       # print("exploding: {}".format("".join([str(x) for x in exploded])))
        return exploded      
    splitted = split(sn)
    if splitted != sn:
       # print("splitting: {}".format("".join([str(x) for x in splitted])))
        
        return splitted
    return sn

def add_snailfish(a, b):
    sn =["["] +  a + b + ["]"]
   ## print(sn)
  #  print("".join([str(x) for x in sn]))
    reducible = True
    while reducible:
        reduced = reduce(sn)
        if reduced != sn:
            sn = reduced.copy()
        else:
            reducible = False
    return sn

def magnitude(snail):
    stack = []
    for c in snail:
        if isinstance(c, int):
            stack.append(c)
        elif c =="[":
            stack.append(c)
        elif c=="]":
            right = stack.pop()
            left = stack.pop()
            stack.pop()
            c =( 2 * right) + (3 * left)
            stack.append(c)
       # print("".join([str(x) for x in stack]))  
        
    assert(len(stack)==1)
    return stack[0]
start = now()
with open("C:/Users/Benaz/Documents/Advent of Code 2021/input.txt") as f:
    lines = [x.strip() for x in f.readlines()]
    snails = [read_snailfish(x) for x in lines]
    largest = 0
    for a,b in itertools.product(snails, repeat=2):
        snail = add_snailfish(a, b)
        mag = magnitude(snail)
        printa = "".join([str(x) for x in a])
        printb = "".join([str(x) for x in b])
       # print("mag: {} + {} = {}".format(printa, printb, mag))
        if mag>largest:
            largest = mag
    print(largest)
    print(now() -start)
    