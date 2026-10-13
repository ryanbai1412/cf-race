from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO; unique, exact token comparison."
STATEMENT = "Legend (syllable = exactly one vowel aeiouy; consonant-only words ignored), input (1<=n<=100, 0<=pi<=100, lines<=100 chars, single spaces), output present."
V = set("aeiouy")


def solve(s):
    lines = s.replace("\r", "").split("\n")
    n = int(lines[0])
    p = list(map(int, lines[1].split()))
    ok = all(sum(c in V for c in lines[2 + i]) == p[i] for i in range(n))
    return "YES\n" if ok else "NO\n"


def line(g, length, alpha):
    words, total = [], -1
    while True:
        w = "".join(g.choice(alpha) for _ in range(g.randint(1, 8)))
        if total + 1 + len(w) > length:
            break
        words.append(w)
        total += 1 + len(w)
    return " ".join(words) or g.choice(alpha)


def make(g, n, length, alpha="abcdeiouyxz", flip=0.5):
    text = [line(g, g.randint(1, length), alpha) for _ in range(n)]
    p = [sum(c in V for c in t) for t in text]
    if g.random() < flip:
        i = g.randrange(n)
        p[i] = (p[i] + g.choice([1, 2, 100])) % 101
    return fmt(n, p, *text)


def cases(g):
    out = [("boundary", "n=1 consonant only, p=0", fmt(1, [0], "bcd")), ("boundary", "n=1 single vowel y", fmt(1, [1], "y")),
           ("adversarial", "y counts as vowel", fmt(2, [2, 0], "yy", "x")), ("adversarial", "off by one", fmt(1, [2], "aeiou")),
           ("maxSize", "n=100 lines of 100 vowels", fmt(100, [100] * 100, *["a" * 100] * 100)),
           ("maxSize", "n=100 random lines length 100", make(g, 100, 100, flip=0.0))]
    out += fill(g, lambda g: make(g, g.randint(1, 4), 12), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), 100), 30)
    return out
