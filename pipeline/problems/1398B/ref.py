import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        s = data[i]
        blocks = sorted((len(b) for b in s.split("0") if b), reverse=True)
        out.append(str(sum(blocks[::2])))
    sys.stdout.write("\n".join(out) + "\n")

main()
