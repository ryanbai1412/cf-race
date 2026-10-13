n,m=map(int,input().split())
lst=list(map(int,input().split()))
res=lst[0] - 1

for i in range(m-1):

    if lst[i] <=lst[i+1]:

        res+= lst[i+1] - lst[i] 

    else:
        res+= n - lst[i] + lst[i+1]

print(res)