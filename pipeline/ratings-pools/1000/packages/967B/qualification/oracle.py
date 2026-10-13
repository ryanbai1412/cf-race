input_list = input().split();
n = int(input_list[0]);
A = int(input_list[1]);
B = int(input_list[2]);

jk= input().split();

list1=[int(s) for s in jk];
    
si  = list1[0];
list1.remove(list1[0]);

list1.sort();
cnt = 0;

S  = si;
num  = n-2;

for it in list1: 
    S +=it;
while num>=0:
    temp = si*A/S;
    if(temp>=B):
        break;
    cnt = cnt+1;
    S = S - list1[num];
    num = num-1;

print(cnt);