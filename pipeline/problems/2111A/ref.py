import sys

def main():
    data = sys.stdin.read().split()
    out = []
    for i in range(int(data[0])):
        x = int(data[1 + i])
        out.append(str(2 * (x.bit_length() - 1) + 3))
    print("\n".join(out))

main()
