n=int(input());c=0;t=[]
for i in input().split():
    i=int(i)
    if i in range(1,n+1):
        if i in t : c+=1
        else : t.append(i)
    else :c+=1
print(c)