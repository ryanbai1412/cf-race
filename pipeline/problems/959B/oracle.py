import sys


class Input:
    def __init__(self):
        data = sys.stdin.buffer.read().replace(b'\r\n', b'\n')
        if b'\r' in data:
            raise ValueError()
        self.lines = data.split(b'\n')
        if self.lines[-1] == b'':
            self.lines.pop()
        self.pos = 0

    def line(self):
        if self.pos == len(self.lines):
            raise ValueError()
        s = self.lines[self.pos]
        self.pos += 1
        return s

    def ints(self, count, lo, hi):
        s = self.line()
        if any(c not in b'0123456789+- \t' for c in s):
            raise ValueError()
        tokens = s.split()
        if len(tokens) != count:
            raise ValueError()
        result = []
        for t in tokens:
            u = t[1:] if t[:1] in (b'+', b'-') else t
            if not u or not u.isdigit():
                raise ValueError()
            u = u.lstrip(b'0') or b'0'
            if len(u) > len(str(max(abs(lo), abs(hi)))):
                raise ValueError()
            v = int(u) * (-1 if t[:1] == b'-' else 1)
            if not lo <= v <= hi:
                raise ValueError()
            result.append(v)
        return result

    def string(self, length, alphabet):
        s = self.line()
        if len(s) != length or any(c not in alphabet for c in s):
            raise ValueError()
        return s

    def end(self):
        if self.pos != len(self.lines):
            raise ValueError()


def solve(r):
    n, k, m = r.ints(3, 1, 100000)
    if k > n:
        raise ValueError()
    words_line = r.line()
    if any(c not in b'abcdefghijklmnopqrstuvwxyz \t' for c in words_line):
        raise ValueError()
    words = words_line.split()
    if len(words) != n or len(set(words)) != n or any(not 1 <= len(w) <= 20 for w in words):
        raise ValueError()
    costs = r.ints(n, 1, 10**9)
    seen = bytearray(n)
    best = [0] * n
    for _ in range(k):
        line = r.line()
        tokens = line.split()
        if not tokens:
            raise ValueError()
        r.pos -= 1
        group = r.ints(len(tokens), 1, n)
        if len(group) != group[0] + 1:
            raise ValueError()
        ids = group[1:]
        price = min(costs[i - 1] for i in ids)
        for i in ids:
            if seen[i - 1]:
                raise ValueError()
            seen[i - 1] = 1
            best[i - 1] = price
    if not all(seen):
        raise ValueError()
    message_line = r.line()
    if any(c not in b'abcdefghijklmnopqrstuvwxyz \t' for c in message_line):
        raise ValueError()
    message = message_line.split()
    if len(message) != m:
        raise ValueError()
    prices = dict(zip(words, best))
    return str(sum(prices[w] for w in message))


if __name__ == '__main__':
    try:
        reader = Input()
        answer = solve(reader)
        reader.end()
    except (ValueError, IndexError, KeyError, OverflowError):
        sys.exit(3)
    if answer:
        sys.stdout.write(answer + '\n')
