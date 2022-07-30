# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 18:37:04 2022

@author: Benazeer
"""

from collections import namedtuple, defaultdict
Point = namedtuple("Point", ["x", "y", "z"])


with open("C:/Users/Benaz/Documents/Advent of Code 2021/input.txt") as f:
    lines = f.readlines()
    scanners = {}
    current = None
    for line in lines:
        if "scanner" in line:
            current = int(line.replace("--- scanner ", "").replace(" ---\n", ""))
            scanners[current] = []
        elif current is not None and not line.isspace():
            pt = Point(*[int(x) for x in line.strip().split(",")])
            scanners[current].append(pt)
    locked = [False] * len(scanners)
    locked[0] = True
    deltas = defaultdict(list)
    for k,v in scanners.items():
        for idx,pt0 in enumerate(v):
            for pt1 in v[idx+1:]:
                if pt0==pt1:
                    continue
                d = (pt1.x - pt0.x)**2 + \
                    (pt1.y - pt0.y)**2 + \
                    (pt1.z - pt0.z)**2
                deltas[k].append((pt1, pt0, d))
    matches = defaultdict(list)
    for k,v in deltas.items():
        if not locked[k]:
            for d in [deltas[x] for x in range(len(scanners)) if locked[x]]:
                print(k,len(d))
                foo = set([x[2] for x in v])
                bar = set([x[2] for x in d])
                print(len(foo.intersection(bar)))
                if len(set([x[2] for x in v]).intersection([x[2] for x in d])) >= 66:
                    locked[k] = True
                    for t0 in v:
                        for t1 in d:
                            if t0[2]==t1[2]:
                                matches[t0[0]].extend(t1[:2])
                                matches[t0[1]].extend(t1[:2])
                                matches[t1[0]].extend(t0[:2])
                                matches[t1[1]].extend(t0[:2])                                
                    
                    
                    
                    
            
        