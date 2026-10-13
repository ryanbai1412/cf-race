from functools import lru_cache
lru_cache(maxsize=None)

t=int(input())
l=[]
temp=0
a,b=map(int,input().split())
c=max(a,b)
for _ in range(t-1):
    a,b=map(int,input().split())
    l.append([a,b])
for a,b in l:
    if min(a,b)<=c:
        if max(a,b)<=c:
            c=max(a,b)
        elif a<=c:
            c=a
        else:
            c=b
            
    else:
        temp=1
        break
print("YES") if temp==0 else print("NO")