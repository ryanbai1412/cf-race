sellers,money=map(int,input().split(' '))
list1=[]
counts=0
list2=[]
index=0
for i in range(sellers):
    array1=list(map(int,input().split(' ')))
    list1.append(array1)
for n in range(len(list1)):
    count=0
    for m in range(1,len(list1[n])):
        if money>list1[n][m]:
            count=1
    if count==1:
        counts+=1
        index=n+1
        list2.append(index)
print(counts)
for f in list2:
    print(f,end=' ')