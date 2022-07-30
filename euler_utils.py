# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:08:37 2021

@author: Benazeer
"""


import itertools
import functools
import math
import operator
import string
import datetime
now = datetime.datetime.now
from collections import defaultdict, Counter
import numbers
import fractions
global gprimes
gprimes = {x:True for x in [2,3,5,7]}
gsieve = [True]*10**5
for k in range(2,10**5):
    if gsieve[k]:
        gprimes[k] = True
        for n in range(k**2, 10**5, k):
            gsieve[n] = False
            


def is_prime(n):
    
    if n<2:
        return False
    if n<4:
        return True
    if n%2==0 or n%3==0:
        return False
    if n<9:
        return True
    if n in gprimes:
        return True
    limit = int(math.sqrt(n))+1
    for k in range(5, limit,6):
        if n%k==0:
            return False
        if n%(k+2)==0:
            return False
    gprimes[n] = True
    return True

def get_gcd(m,n):
    a = max(m,n)
    b = min(m,n)
    R = a%b
    while R>0:
        a = b
        b = R
        R = a%b
    return b
#phi(n) = n * Prod_(p|n)(1 - 1/p)
# where p|n denotes distinct primes that evenly divide n

# for problem 69 and 70, n/phi(n) the optimication function is
# 1/Prod(1-1/p)
# 1/(Prod((p-1)/p))
# Prod(p/(p-1))
# maximize for 69 (as many p as possible)
# minimize for 70 (as few p as possible)

def totient(n, prime):
    if is_prime(n):
        return n-1
    ntest = n
    pfactors = set()
    limit = int(math.sqrt(n))
    if max(prime.get_primes()) < limit:
        for k in range(max(prime.get_primes())+2, limit+1, 2):
            prime.isprime(k)
    for p in prime.get_primes():
        if p > ntest:
            break
        if ntest%p==0:
            pfactors.add(p)
            if is_prime(n/p):
                pfactors.add(int(n/p))
            while ntest%p==0:
                ntest = ntest//p
    prod = functools.reduce(operator.mul, [1-1/p for p in pfactors], n)
    return int(prod)
    

class PrimeTools:
    
    
    def __init__(self):
        self.primes = {2:True}
        self.largest_sieved_prime = 2
        self.sieve = [True]*10**5
        for idx in range(2, 10**5):
            if self.sieve[idx]:
                for k in range(idx**2, 10**5, idx):
                    self.sieve[k] = False
                self.primes[idx]= True
        self.largest_sieved_prime = max([k for k in self.primes.keys()])


    def isprime(self,n):
        if n<2:
            return False
        if n<4:
            return True
        if n%2==0 or n%3==0:
            return False
        if n<len(self.sieve):
            return self.sieve[n]
        
        if n in self.primes:
            return True
        
        limit = int(math.sqrt(n))
        
        for k in range(5, limit+1, 6):
            if n%k==0:
                return False
            if n%(k+2)==0:
                return False
        else:
            self.primes[n] = True
            return True
        
    def get_plist(self):
        return list(sorted(self.primes.keys()))
    
    def get_primes(self):
        return sorted(self.primes.keys())
    
    def extend_sieve(self, n):
       for k in range(self.largest_sieved_prime+2,self.largest_sieved_prime+n, 2):
           if self.isprime(k):
               self.largest_sieved_prime = k
            
        
        
prime = PrimeTools()

def reverse(n):
    rev = 0
    if n<10:
        return n
    while n > 0:
        r = n%10
        rev = 10*rev + r
        n = n//10
    return rev


def get_digits(n):
    if n < 10:
        return [n]
    digits = [n%10]
    n = n//10
    while n>0:
        r = n%10
        digits.insert(0, int(r))
        n=n//10
    return digits

def has_duplicated_digits(n):
    if n>=10**10:
        return True
    n = str(n)
    for c in n:
        if n.count(c) > 1:
            return True
    return False
def is_palindrome(n):
    if isinstance(n,int):
        if n == reverse(n):
            return  True
        else:
            return False 
    if isinstance(n, str):
        if n == n[::-1]:
            return True
        else:
            return False

def quadratic(a,b,c):
    det = math.sqrt(b**2 - (4*a*c))
    n1 = (-b + det)/(2*a)
    n2 = (-b - det)/(2*a)
    return(n1, n2)

def quadratic_integer_soln(a,b,c):
    n1,n2 = quadratic(a,b,c)
    for n in [n1,n2]:
        if n>0 and n == int(n):
            return int(n)
    return False

def triangle(n):
    return int((n/2)*(n+1))
# t = (1/2) n * (n+1) 
# 2t = n^2 + n
def is_triangle(t):
    return (quadratic_integer_soln(1, 1, -2*t))
    
def pentagon(n):
    return int(n*(3*n-1)/2)
# 2p = 3n^2 - n
def is_pentagon(p):
    return quadratic_integer_soln(3, -1, -2*p)


def hexagon(n):
    return int(n*(2*n-1))
# h = 2n^2-n
def is_hexagon(h):
    return quadratic_integer_soln(2, -1, -h)

print(now().strftime("%H:%M:%S"))

coins = [1,2,5,10,20,50,100,200]
coinways = {(1,1): 1}
tot = 200
remtot = 200
ways = 0

def get_ways(coins, tot):
    ways = 0
    maxcoin = max(coins)
    coins = [c for c in coins if c<=tot]
    if (tot, maxcoin) in coinways:
        return coinways[(tot, maxcoin)]
    coins.sort()
    for c in reversed(coins):
        
        if c > tot:
           # print("{}p too large, skipping".format(c))
            continue
        if tot%c==0:
           # print("{} can be made with {} {}p coins. ++1".format(tot, tot//c, c))
            ways+=1
        remtot = tot - c
        coins.remove(c)
        if len(coins) ==0:
            break
        while remtot > 0:
          #  print("Adding ways to make {} without a {}p piece".format(remtot,c))
            ways+=(get_ways(coins, remtot))
            remtot -= c
    coinways[(tot, maxcoin)] = ways
    return ways

partition_function_memo = [1,1]

def partition_function(n):
    if n < 0:
        return 0
    if n<2:
        return 1
    if n!=int(n):
        raise
    n = int(n)
    if n <len(partition_function_memo):
        return partition_function_memo[n]
    if n == len(partition_function_memo):
        s = 0
        for k in range(1, n+1):
            if k%2:
                sign = 1
            else:
                sign = -1
            arg1 = n - (k/2)*(3*k-1)
            arg2 = n - (k/2)*(3*k+1)
            addend = 0
            if arg1<0 and arg2<0:
                break
            for a in [arg1, arg2]:
                if a >=0:
                    addend += partition_function_memo[int(a)]
            addend = addend * sign
            s+=addend
            
                
        partition_function_memo.append(s%1000000) 
        return s
    else:
        for k in range(len(partition_function_memo), n+1):
            partition_function(k)
        return partition_function_memo[n]



phi = (1 + math.sqrt(5))/2
psi = 1 - phi




def fibinv(F):
    arg = F*math.sqrt(5) + .5
    return int(math.log(arg, phi))

def is_pandigital(n):
    last_nine = []
    d,r = divmod(n,10)
    while len(last_nine)<9:
        if r==0:
            return False
        last_nine.append(r)
        d,r = divmod(d,10)
        
    return len(set(last_nine))==9

def fib(n):
    if n<1:
        raise ValueError
    if n<3:
        return 1
    f1 = 1
    f2 = 1
    for k in range(3, n+1):
        f3 = f2+f1
        f1 = f2
        f2 = f3
    return f3
startTime = now()

def get_anagrams(sequence):
    anagrams = []
    if len(sequence)==0:
        return anagrams
    if isinstance(sequence[0], int):
        sequence = [str(x) for x in sequence]
    while len(sequence):
        this_set = []
        w = sequence.pop(0)
        for other in sequence:
            if sorted(w)==sorted(other):
                this_set.append(other)
        if len(this_set):
            for found in this_set:
                sequence.remove(found)
            this_set.append(w)
        
            anagrams.append(this_set)
    return anagrams

def isanagram(x, y):
    if isinstance(x,int):
        x = str(x)
        y = str(y)
    return sorted(x)==sorted(y)


def is_s_number(n):
    digs = get_digits(n)
    rt = int(math.sqrt(n))
    if rt**2 != n:
        raise ValueError
    if sum(digs) == rt:
        return True
    elif len(digs)==2:
        return False
        
    masks = []
    for k in range(2, len(digs)):
        loops = len(digs)//k
        for ll in range(1, loops+1):
            m = []
            
    for m in masks:
        s = 0
        for places in m:
            if len(places)==1:
                s+=digs[places[0]]
            elif len(places) == 2:
                tmp = 10*digs[places[0]] + digs[places[1]]
                s+=tmp
            elif len(places)==3:
                tmp = 100*digs[places[0]]
                tmp += 10*digs[places[1]]
                tmp += digs[places[2]]
                s+= tmp
            else:
                print("Error: ", m, s, digs)
                raise AssertionError
        if s==rt:
            return True
    else:
        return False

    

# eulercoin_multiple = 1_504_170_715_041_707
# eulercoin_modulus = 4_503_599_627_370_517
# coins = []
# indices = []
# prev_element = 0 
# current_smallest= 0
# n = 1
# while current_smallest > 1:
#     element = (prev_element + eulercoin_multiple) % eulercoin_modulus
#     if element < current_smallest:
#         current_smallest = element
#         coins.append(element)
#         indices.append(n)
#         print(now()-startTime, len(coins))
#         if n>=3:
#             # delta = indices[-1] - indices[-2]
#             # prev_element = element + (delta-1)*eulercoin_multiple 
#             # n += delta -1
#      #       delta = math.floor((current_smallest + eulercoin_multiple)/overshoot)
#             prev_element = element + ()
#             # continue
#             # coin * n < k*modulus + smallestc
#     if element==1:
#         break
#     prev_element = element
#     n+=1


N = 23
a = []
def find_repeats(a):
    if len(a)<2:
        return False
    for i in range(math.floor(len(a)/2)):  
        if a[0:i+1] == a[i+1:2*i+2]:
           
            return True
    return False

def get_continued_fraction(N):
    a0 = math.floor(N)
    if a0==N:
        return 0
    rem = N - a0
    count = 0
    while True:
        invert = 1/rem
        nexta = math.floor(invert)
        rem = invert - nexta
        count +=1
        if nexta==a0*2:
            return count

count = 0
    
for N in range(2, 10001 ):
    a = get_continued_fraction(math.sqrt(N))
    if a%2:
        count+=1
print(count)
    
    
print(now()-startTime)
    