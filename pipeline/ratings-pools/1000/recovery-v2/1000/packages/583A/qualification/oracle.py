n=int(input())
a,b=[0,0]*n,[0,0]*n
for i in range(n*n):
  x,y=map(int,input().split())
  if a[x]<1>b[y]:a[x]=b[y]=1;print(i+1,end=' ')