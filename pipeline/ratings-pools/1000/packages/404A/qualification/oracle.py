n=int(input())
a=""
f,s="",""
for i in range(n):
    letters=input()
    if i==0:
        f=letters[0]
        s=letters[1]
    if i==n//2:
        if  letters.count(f) !=1 or letters.count(s)!=n-1 :
            a="NO"
    else:
        if letters.count(f)!=2 or letters.count(s)!=n-2:
            a="NO"

print("YES" if a=="" else a)