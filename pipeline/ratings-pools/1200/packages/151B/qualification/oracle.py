import sys
import re


def integer(word):
    assert re.fullmatch(rb'[+-]?[0-9]+', word)
    sign = -1 if word.startswith(b'-') else 1
    digits = word.lstrip(b'+-').lstrip(b'0') or b'0'
    assert len(digits) <= 16
    return sign * int(digits)


class Reader:
    def __init__(self, data):
        data = data.replace(b'\r\n', b'\n')
        assert b'\r' not in data
        self.lines = data.split(b'\n')
        if data.endswith(b'\n'):
            self.lines.pop()
        self.index = 0

    def line(self):
        assert self.index < len(self.lines)
        value = self.lines[self.index]
        self.index += 1
        return value

    def ints(self, count, low, high):
        line = self.line()
        assert re.fullmatch(rb'[0-9+\- \t]+', line)
        words = line.split()
        assert len(words) == count
        values = [integer(w) for w in words]
        assert all(low <= x <= high for x in values)
        return values

    def word(self, pattern, low, high):
        value = self.line()
        assert low <= len(value) <= high
        assert re.fullmatch(pattern, value)
        return value

    def end(self):
        assert self.index == len(self.lines)


def solve(data):
    p = Reader(data)
    n, = p.ints(1, 1, 100)
    names, counts = [], []
    for _ in range(n):
        header_line = p.line()
        assert re.fullmatch(rb'[ \t]*[+-]?[0-9]+[ \t]+[a-zA-Z]+[ \t]*', header_line)
        header = header_line.split()
        assert len(header) == 2
        size = integer(header[0])
        assert 0 <= size <= 100 and 1 <= len(header[1]) <= 20
        names.append(header[1].decode('ascii'))
        count = [0, 0, 0]
        for _ in range(size):
            phone = p.word(rb'[0-9]{2}-[0-9]{2}-[0-9]{2}', 8, 8)
            digits = phone.replace(b'-', b'')
            kind = 0 if len(set(digits)) == 1 else (1 if all(digits[i] > digits[i + 1] for i in range(5)) else 2)
            count[kind] += 1
        counts.append(count)
    phrases = ('If you want to call a taxi, you should call: ',
               'If you want to order a pizza, you should call: ',
               'If you want to go to a cafe with a wonderful girl, you should call: ')
    lines = []
    for kind, phrase in enumerate(phrases):
        maximum = max(c[kind] for c in counts)
        lines.append(phrase + ', '.join(names[i] for i in range(n) if counts[i][kind] == maximum) + '.')
    answer = '\n'.join(lines)
    p.end()
    return str(answer) + '\n'


if __name__ == '__main__':
    try:
        result = solve(sys.stdin.buffer.read())
    except (AssertionError, ValueError, IndexError):
        sys.exit(3)
    sys.stdout.write(result)
