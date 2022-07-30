 # -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 15:45:23 2022

@author: Benazeer
"""
import datetime
now = datetime.datetime.now
xconsts = [11,13,11,10,-3,-4,12,-8,-3,-12,14,-6,11,-12]
yconsts = [14,8,4,10,14,10,4,14,1,6,0,9,13,12]
zconsts = [1,1,1,1,26,26,1,26,26,26,1,26,1,26]
def monad(lastz, inp, i):
    x =( lastz % 26) + xconsts[i]
    #print(x)
    z = lastz //zconsts[i]
    if x!=inp:
        z = (26 * z) + inp + yconsts[i]
    return z

def reverse_monad(outp, inp, i):
    # if x != inp:
    z, m = divmod(outp - inp -yconsts[i], 26)
    possibles =[]
    if m==0:
        lastz = range(z*zconsts[i], (z+1)*zconsts[i])
        for posz in lastz:
            x = (posz % 26) + xconsts[i]
            if x!=inp:
                possibles.append(posz)
    lastz = range(outp*zconsts[i], (outp+1)*zconsts[i])
    for posz in lastz:
        x = (posz % 26) + xconsts[i]
        if x ==  inp:
            possibles.append(posz)
    return possibles
inputs = [[0]]
start = now()


for i in range(13, -1, -1):
    newinputs = []
    print(i, len(inputs), now()-start)
    
    for inp in inputs:
        for ct in range(1, 10):
            possibles = reverse_monad(inp[0], ct, i)
            for p in possibles:
                newinp = [p, ct]
                newinp.extend(inp[1:])
                newinputs.append(tuple(newinp))
               
   # print(i, max([x[0] for x in newinputs]))
    inputs = newinputs.copy()
print(now()-start)   
print(len(inputs))

inputs = [int("".join([str(x) for x in y] )) for y in inputs]
print(max(inputs))
print(min(inputs))
print(now() - start)