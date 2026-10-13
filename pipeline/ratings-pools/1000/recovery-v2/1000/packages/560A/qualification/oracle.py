def main():
    n = int(input())
    a = input().split()
    for c in a:
        if c == "1":
            return -1
    return 1

print(main())