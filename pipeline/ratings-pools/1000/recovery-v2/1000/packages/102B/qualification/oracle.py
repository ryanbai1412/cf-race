number = list(input().strip())
cast_spell = 0
length = len(number)

while length > 1:
    summation = 0
    for digit in number:
        summation += int(digit)
    number = list(str(summation))
    length = len(number)
    cast_spell += 1

print(cast_spell)