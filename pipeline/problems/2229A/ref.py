import sys

def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        out.append(str((max(a) - min(a) + 1) // 2))
    print("\n".join(out))

main()
