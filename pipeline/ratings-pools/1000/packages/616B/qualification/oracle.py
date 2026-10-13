n,m=map(int,input().split())
z=[]
a=[]
for i in range(n):
    a=list(map(int,input().split()))
    z.append(min(a))
print(max(z))