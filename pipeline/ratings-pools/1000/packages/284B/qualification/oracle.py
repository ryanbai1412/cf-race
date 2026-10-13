n = int(input())
x = input()

if x.count('I') == 0:
	print(n - x.count('F'))
elif x.count('I') == 1:
	print(1)
else:
	print(0)