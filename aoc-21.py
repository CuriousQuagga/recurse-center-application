# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 22:45:00 2022

@author: Benazeer
"""
from collections import defaultdict, namedtuple, Counter

from math import inf, sqrt
Point = namedtuple('Point', ['x', 'y', 'z'])
import datetime
now = datetime.datetime.now
import itertools
import operator
start = now()
rolls = [3, 4, 5, 4, 5, 6, 5, 6, 7, 4, 5, 6, 5, 6, 7, 6, 7, 8, 5, 6, 7, 6, 7, 8, 7, 8, 9]
rf = Counter(rolls)

testinput = True
def take_turn( space, roll, score):
    space = (space + roll) % 10
    score = score + space + 1
    return (space, score)

def deterministic_game(p1_loc, p2_loc):
    c = itertools.count(1, 3)
    p1_score = 0
    p2_score = 0
    turn = 1
    count = 0
    while p1_score <1000 and p2_score < 1000:
        roll = next(c)
        if roll >=98:
            m1 = roll
            m2 = roll + 1
            if m2 > 100:
                m2 = m2%100
                
            m3 = roll + 2
            if m3 > 100:
                m3 = m3%100
                
            move = m1 + m2 + m3
            if m3==100:
                n = 1
            else:
                n = m3+1
            c = itertools.count(n, 3)
        else:
            move = 3*roll  + 3 
        if turn==1:
            p1_loc, p1_score = take_turn(p1_loc, move, p1_score)
            turn = 2
        elif turn==2:
            p2_loc, p2_score = take_turn(p2_loc, move, p2_score)
            turn = 1
        
        count +=3
        print(roll, p1_score, p2_score, count)
    loser = min(p1_score, p2_score)
    print(loser * count)
def recurse_game(p1_loc, p1_score, p2_loc, p2_score):
    if p2_score >= 21:
        return (0,1)
    w1 = 0
    w2 = 0
    for r, f in rf.items():
        p1l, p1s = take_turn(p1_loc, r, p1_score)
        tmp2, tmp1 = recurse_game(p2_loc, p2_score, p1l, p1s)
        w1 += tmp1 * f
        w2 += tmp2 * f
    #print("universe starting P1 at {},{}; P2 at {},{}, wins are {},{}".format(p1_loc, p1_score, p2_loc, p2_score, w1, w2))
    return(w1, w2)

p1_start = 1
p2_start = 4
testinput= False
w1, w2 = recurse_game(p1_start,0, p2_start,0)
   
print(now() - start)
print(w1, w2)
if testinput:
    assert(max(w1,w2)==444356092776315)

    
    

