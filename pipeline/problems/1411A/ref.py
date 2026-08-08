import sys

def main():
    data = sys.stdin.read().split()
    pos = 1
    out = []
    for _ in range(int(data[0])):
        n = int(data[pos]); s = data[pos + 1]; pos += 2
        k = len(s) - len(s.rstrip(")"))
        out.append("Yes" if k > n - k else "No")
    sys.stdout.write("\n".join(out) + "\n")

main()
