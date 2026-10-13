n=int(input())
l=list(map(int,input().split()))
l.sort()
maxa=0
x=l[0]
count=0
towers=1
for i in l:
    if(i==x):
        count+=1
        if(count>maxa):
            maxa=count
    else:
        count=1
        towers+=1
        x=i
print(maxa,towers)