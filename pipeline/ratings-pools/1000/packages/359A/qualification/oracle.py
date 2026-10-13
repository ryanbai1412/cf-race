n, m = map(int, input().split())
a = []
number_of_operations = 0

for _ in range(n):
    row = input().split()
    a.append(row)
    if row[0] == '1' or row[-1] == '1':
        number_of_operations = 2

if '1' in a[0] or '1' in a[-1]:
    number_of_operations = 2

print(4 if not(number_of_operations) else 2)