import sys

def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(int(data[0])):
        n = int(data[1 + i])
        out.append("0" if n % 2 else str(n // 4 + 1))
    print("\n".join(out))

main()
