n = int(input())
arr = list(map(int, input().split(" ")))

count5 = 0
count0 = 0

for i in range(len(arr)):
    if arr[i] == 5:
        count5 += 1
    else:
        count0 += 1

if count0 == 0:
    print(-1)

elif count5 < 9:
    print(0)

else:
    count5 -= count5 % 9
    for i in range(count5):
        print("5", end="")
    for i in range(count0):
        print("0", end="")