n=int(input())
h=0
t=0
for j in range(n):
    hi = int(input())
    if(j==0):
        h=hi
        t+=(hi+1)
    else:
        t+=(abs(hi-h)+2)
        h=hi 
    # print(t)
print(t)