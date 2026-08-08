import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); k = int(data[pos + 1]); pos += 2
        a = list(map(int, data[pos:pos + n])); pos += n
        mn = min(a)
        total = 0
        seen_min = False
        for x in a:
            if x == mn and not seen_min:
                seen_min = True
                continue
            total += (k - x) // mn
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")

main()
