import sys

def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); pos += 1
        a = list(map(int, data[pos:pos + n])); pos += n
        best = 0
        for j in range(n):
            left = j  # length of prefix segment before the gap at j-1
            right = n - j - 1  # elements after j; usable segment length right-1... see below
            lcnt = (j - 1 + 1) // 2 if j >= 1 else 0          # ceil((j-1)/2) over indices 0..j-2
            rcnt = (n - j - 2 + 1) // 2 if n - j - 2 >= 1 else 0  # ceil((n-j-2)/2) over j+2..n-1
            best = max(best, a[j] + 1 + lcnt + rcnt)
        out.append(str(best))
    print("\n".join(out))

main()
