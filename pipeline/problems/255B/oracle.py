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
    s = r.line()
    if not 1 <= len(s) <= 10**6 or any(c not in b'xy' for c in s):
        raise ValueError()
    balance = 2 * s.count(b'x') - len(s)
    if balance == 0:
        raise ValueError()
    return ('x' if balance > 0 else 'y') * abs(balance)


if __name__ == '__main__':
    try:
        reader = Input()
        answer = solve(reader)
        reader.end()
    except (ValueError, IndexError, KeyError, OverflowError):
        sys.exit(3)
    if answer:
        sys.stdout.write(answer + '\n')
