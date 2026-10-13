op=int(input())
x=0
y=0
z=0
for i in range(0,op):
    ab=input()
    mn=ab.split()
    l=int(mn[0])
    m=int(mn[1])
    n=int(mn[2])
    x=l+x
    y=m+y
    z=n+z
if x==0 and y==0 and z==0:
    print("YES")
else:
    print("NO")