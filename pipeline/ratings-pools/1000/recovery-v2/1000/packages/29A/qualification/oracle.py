from collections import *
# from math import ceil, gcd,inf
from functools import *
import sys
input = lambda: sys.stdin.readline().rstrip()  # faster!

Z=int(input())
arr=set()
for _ in range(Z):
    i,d=map(int,input().split())
    arr.add(tuple(sorted((i,i+d))))
# print(arr)    
print('yes' if len(arr) != Z else 'no')