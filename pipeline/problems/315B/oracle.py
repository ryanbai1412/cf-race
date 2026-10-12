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
    n, m = r.ints(2, 1, 100000)
    a = r.ints(n, 1, 10**9)
    offset = 0
    answers = []
    for _ in range(m):
        line = r.line()
        tokens = line.split()
        if not tokens:
            raise ValueError()
        r.pos -= 1
        values = r.ints(len(tokens), 1, 10**9)
        if values[0] == 1:
            if len(values) != 3:
                raise ValueError()
            t, v, x = values
            if v > n:
                raise ValueError()
            a[v - 1] = x - offset
        elif values[0] == 2:
            if len(values) != 2:
                raise ValueError()
            t, y = values
            if y > 10000:
                raise ValueError()
            offset += y
        elif values[0] == 3:
            if len(values) != 2:
                raise ValueError()
            t, q = values
            if q > n:
                raise ValueError()
            answers.append(str(a[q - 1] + offset))
        else:
            raise ValueError()
    return '\n'.join(answers)


if __name__ == '__main__':
    try:
        reader = Input()
        answer = solve(reader)
        reader.end()
    except (ValueError, IndexError, KeyError, OverflowError):
        sys.exit(3)
    if answer:
        sys.stdout.write(answer + '\n')
