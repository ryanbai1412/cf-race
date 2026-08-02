import sys

def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + 2 * n])); pos += 2 * n
        ones = sum(a)
        zeros = 2 * n - ones
        out.append(f"{ones % 2} {min(ones, zeros)}")
    print("\n".join(out))

main()
