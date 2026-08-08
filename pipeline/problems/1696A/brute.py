"""Independent brute force: BFS over full (a, z) states (tiny inputs only)."""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); z = int(data[pos + 1]); pos += 2
        a = tuple(int(x) for x in data[pos:pos + n]); pos += n
        start = (a, z)
        seen = {start}
        stack = [start]
        best = max(a)
        while stack:
            arr, zz = stack.pop()
            best = max(best, max(arr))
            for i in range(n):
                na = arr[:i] + (arr[i] | zz,) + arr[i + 1:]
                nz = arr[i] & zz
                st = (na, nz)
                if st not in seen:
                    seen.add(st)
                    stack.append(st)
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
