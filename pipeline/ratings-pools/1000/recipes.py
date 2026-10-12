"""Authored deterministic tests, strict input checks and integer/token oracles."""
from collections import Counter, deque
import itertools
import math
import random
import re
from input_layout import layout

IDS = ("139A", "108A", "742A", "626A", "450A", "979A", "114A", "680B",
       "622A", "777A", "479A", "75A", "131A", "17A", "515A", "577A",
       "58A", "1036A", "124A", "476A", "859B", "659A")

RULES = {
    "139A": "n=1..1000; seven capacities in0..1000 with positive sum; simulate cyclic reading; unique finishing weekday.",
    "108A": "Exactly HH:MM,00<=HH<=23,00<=MM<=59; search strictly later, wrapping at midnight; unique nearest palindrome.",
    "742A": "n=0..10^9; exact modular exponentiation1378^n mod10; unique digit.",
    "626A": "n=1..200 and exactly n U/R/D/L letters; count equal pairs of prefix coordinates; unique integer.",
    "450A": "n,m=1..100; exactly n needs in1..100; queue simulation with m-candy rounds; unique last child, including ties.",
    "979A": "n=0..10^18; n+1 congruent radial sectors; zero cuts for one sector, diameters halve even sector counts; otherwise one cut per boundary.",
    "114A": "k,l=2..2^31-1; only l=k^e,e>=1 yields YES and importance e-1; otherwise NO; integer powers only.",
    "680B": "1<=a<=n<=100; exactly n bits; at each distance catch criminals only if every city at that distance has one.",
    "622A": "n=1..10^14; exact integer triangular-block search; unique offset within1..block; no floating arithmetic.",
    "777A": "n=1..2*10^9,x=0..2; six swaps form identity; invert the remaining swaps in reverse chronological order.",
    "479A": "Three integers in1..10; enumerate ordered binary expression trees using+/*; unique maximum, no reordering.",
    "75A": "Two positive integers in1..10^9; remove zero digits from both operands and their sum, then test equality.",
    "131A": "1..100 ASCII Latin letters; invert all cases iff every character after the first is uppercase, including one-letter inputs.",
    "17A": "n=2..1000,k=0..1000; sieve primes and count primes equal to neighboring prime sums plus1; threshold predicate.",
    "515A": "a,b=-10^9..10^9,s=1..2*10^9; Manhattan distance <=s and even remaining steps; YES/NO is case-insensitive.",
    "577A": "n=1..10^5,x=1..10^9; enumerate first coordinate divisors with second coordinate <=n; unique count.",
    "58A": "1..100 lowercase ASCII letters; greedy subsequence hello; unique YES/NO.",
    "1036A": "n,k=1..10^18; n independent integer-height triangles each of base2 contribute their height as area; answer ceil(k/n).",
    "124A": "0<=a,b<n<=100; enumerate positions with at least a predecessors and at most b successors; unique count.",
    "476A": "n=1..10000,m=2..10; enumerate feasible move counts ceil(n/2)..n and minimize those divisible by m; -1 if none.",
    "859B": "N=1..10^6; search integer bounding rectangle sides with area>=N; min2*(width+height). Removing final excess corner cells realizes areaN without increasing perimeter.",
    "659A": "n=1..100,a=1..n,b=-100..100; step around cyclic entrances in signed direction; unique entrance.",
}


def integers(text, count=None):
    tokens = text.split()
    if not tokens or any(not re.fullmatch(r"-?\d+", t) for t in tokens):
        raise ValueError("noninteger input")
    values = list(map(int, tokens))
    if count is not None and len(values) != count:
        raise ValueError("wrong integer count")
    return values


def within(value, low, high):
    if not low <= value <= high:
        raise ValueError(f"integer outside [{low},{high}]: {value}")


def output(pid, text):
    if pid in ("108A", "131A", "58A"):
        words = text.split()
        if len(words) != 1:
            raise ValueError("expected one word")
        word = words[0]
        if pid == "108A":
            if not re.fullmatch(r"\d{2}:\d{2}", word):
                raise ValueError("invalid time format")
            hour, minute = map(int, word.split(":"))
            within(hour, 0, 23)
            within(minute, 0, 59)
            now = hour * 60 + minute
            for step in range(1, 1441):
                t = (now + step) % 1440
                candidate = f"{t//60:02}:{t%60:02}"
                if candidate == candidate[::-1]:
                    return candidate + "\n"
        if not re.fullmatch(r"[A-Za-z]{1,100}" if pid == "131A" else r"[a-z]{1,100}", word):
            raise ValueError("invalid word")
        if pid == "131A":
            return (word.swapcase() if all(c.isupper() for c in word[1:]) else word) + "\n"
        cursor = 0
        for c in word:
            if cursor < 5 and c == "hello"[cursor]:
                cursor += 1
        return ("YES" if cursor == 5 else "NO") + "\n"
    if pid == "626A":
        words = text.split()
        if len(words) != 2 or not words[0].isdigit():
            raise ValueError("invalid robot input")
        n, commands = int(words[0]), words[1]
        within(n, 1, 200)
        if len(commands) != n or set(commands) - set("URDL"):
            raise ValueError("invalid robot commands")
        positions = Counter({(0, 0): 1})
        x = y = answer = 0
        for c in commands:
            dx, dy = {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}[c]
            x, y = x + dx, y + dy
            answer += positions[x, y]
            positions[x, y] += 1
        return f"{answer}\n"
    v = integers(text)
    counts = {"139A": 8, "742A": 1, "979A": 1, "114A": 2, "622A": 1,
              "777A": 2, "479A": 3, "75A": 2, "17A": 2, "515A": 3,
              "577A": 2, "1036A": 2, "124A": 3, "476A": 2, "859B": 1, "659A": 3}
    if pid in counts and len(v) != counts[pid]:
        raise ValueError("wrong integer count")
    if pid == "139A":
        n, *days = v
        within(n, 1, 1000)
        for d in days:
            within(d, 0, 1000)
        if sum(days) == 0:
            raise ValueError("no reading capacity")
        i = 0
        while n > 0:
            n -= days[i % 7]
            i += 1
        answer = (i - 1) % 7 + 1
    elif pid == "742A":
        n, = v
        within(n, 0, 10**9)
        answer = pow(1378, n, 10)
    elif pid == "450A":
        n, m, *needs = v
        within(n, 1, 100)
        within(m, 1, 100)
        if len(needs) != n:
            raise ValueError("wrong needs count")
        for a in needs:
            within(a, 1, 100)
        queue = deque(enumerate(needs, 1))
        while queue:
            answer, remaining = queue.popleft()
            if remaining > m:
                queue.append((answer, remaining - m))
    elif pid == "979A":
        n, = v
        within(n, 0, 10**18)
        answer = 0 if n == 0 else (n + 1) // 2 if n % 2 else n + 1
    elif pid == "114A":
        k, l = v
        within(k, 2, 2**31 - 1)
        within(l, 2, 2**31 - 1)
        value, exponent = k, 1
        while value < l:
            value *= k
            exponent += 1
        return f"YES\n{exponent-1}\n" if value == l else "NO\n"
    elif pid == "680B":
        n, a, *bits = v
        within(n, 1, 100)
        within(a, 1, n)
        if len(bits) != n or set(bits) - {0, 1}:
            raise ValueError("invalid criminal bits")
        answer = 0
        for distance in range(n):
            cities = {a - 1 - distance, a - 1 + distance} & set(range(n))
            if cities and all(bits[i] for i in cities):
                answer += len(cities)
    elif pid == "622A":
        n, = v
        within(n, 1, 10**14)
        left, right = 1, n
        while left < right:
            mid = (left + right) // 2
            if mid * (mid + 1) // 2 >= n:
                right = mid
            else:
                left = mid + 1
        answer = n - left * (left - 1) // 2
    elif pid == "777A":
        n, x = v
        within(n, 1, 2 * 10**9)
        within(x, 0, 2)
        for step in range(n % 6, 0, -1):
            a, b = (0, 1) if step % 2 else (1, 2)
            if x in (a, b):
                x = a + b - x
        answer = x
    elif pid == "479A":
        for x in v:
            within(x, 1, 10)
        def expressions(values):
            if len(values) == 1:
                return {values[0]}
            answers = set()
            for split in range(1, len(values)):
                for a in expressions(values[:split]):
                    for b in expressions(values[split:]):
                        answers.update((a + b, a * b))
            return answers
        answer = max(expressions(v))
    elif pid == "75A":
        a, b = v
        within(a, 1, 10**9)
        within(b, 1, 10**9)
        def no_zeros(x):
            return int(str(x).replace("0", ""))
        return ("YES" if no_zeros(a) + no_zeros(b) == no_zeros(a + b) else "NO") + "\n"
    elif pid == "17A":
        n, k = v
        within(n, 2, 1000)
        within(k, 0, 1000)
        prime = [True] * (n + 1)
        prime[:2] = [False, False]
        for p in range(2, math.isqrt(n) + 1):
            if prime[p]:
                for multiple in range(p*p, n+1, p):
                    prime[multiple] = False
        ps = [p for p in range(2, n+1) if prime[p]]
        good = sum(a+b+1 <= n and prime[a+b+1] for a, b in zip(ps, ps[1:]))
        return ("YES" if good >= k else "NO") + "\n"
    elif pid == "515A":
        a, b, s = v
        within(a, -10**9, 10**9)
        within(b, -10**9, 10**9)
        within(s, 1, 2*10**9)
        distance = abs(a) + abs(b)
        return ("YES" if s >= distance and (s-distance) % 2 == 0 else "NO") + "\n"
    elif pid == "577A":
        n, x = v
        within(n, 1, 10**5)
        within(x, 1, 10**9)
        answer = sum(x % i == 0 and x//i <= n for i in range(1, min(n, x)+1))
    elif pid == "1036A":
        n, k = v
        within(n, 1, 10**18)
        within(k, 1, 10**18)
        answer = (k+n-1)//n
    elif pid == "124A":
        n, a, b = v
        within(n, 1, 100)
        within(a, 0, n-1)
        within(b, 0, n-1)
        answer = sum(p >= a and n-1-p <= b for p in range(n))
    elif pid == "476A":
        n, m = v
        within(n, 1, 10000)
        within(m, 2, 10)
        answer = next((moves for moves in range((n+1)//2, n+1) if moves % m == 0), -1)
    elif pid == "859B":
        n, = v
        within(n, 1, 10**6)
        answer = min(2*(width + (n+width-1)//width) for width in range(1, math.isqrt(n)+2))
    elif pid == "659A":
        n, a, b = v
        within(n, 1, 100)
        within(a, 1, n)
        within(b, -100, 100)
        for _ in range(abs(b)):
            a += 1 if b > 0 else -1
            if a == n+1:
                a = 1
            if a == 0:
                a = n
        answer = a
    else:
        raise ValueError("unowned recipe")
    return f"{answer}\n"


def extra_inputs(pid):
    rng = random.Random(int.from_bytes(pid.encode(), "big"))
    cases = []
    def add(*values):
        cases.append(" ".join(map(str, values)) + "\n")
    if pid == "139A":
        for day in range(7):
            for n in (1, 999, 1000):
                days = [0]*7
                days[day] = 1 if n != 999 else 1000
                add(n, *days)
        for _ in range(20):
            add(rng.randint(1,1000), *[rng.randint(0,10) for _ in range(7)])
        add(1000, *[1000]*7)
    elif pid == "108A":
        cases = [f"{h:02}:{m:02}\n" for h, m in [(0,0),(0,1),(23,59),(23,32),(23,33),(15,51),(5,50),(5,51),(11,11),(12,21),(22,22),(1,9),(1,10)]]
        cases += [f"{rng.randrange(24):02}:{rng.randrange(60):02}\n" for _ in range(25)]
    elif pid == "742A":
        for n in list(range(20)) + [10**9-i for i in range(8)]:
            add(n)
    elif pid == "626A":
        words = ["U","LR","URDL","UUDDLLRR","UD"*100,"UR"*100,"U"*200,"U"*100+"D"*100,"LR"*99+"UD"]
        words += ["".join(rng.choice("URDL") for _ in range(n)) for n in (2,3,5,10,50,99,100,199,200)]
        cases = [f"{len(w)}\n{w}\n" for w in words]
    elif pid == "450A":
        add(1,1,1)
        add(1,1,100)
        add(100,1,*[100]*100)
        add(100,100,*[1]*100)
        add(5,3,1,2,3,3,1)
        add(3,3,7,9,8)
        add(3,3,10,9,8)
        for _ in range(20):
            n,m=rng.randint(1,100),rng.randint(1,100)
            add(n,m,*[rng.randint(1,100) for _ in range(n)])
    elif pid == "979A":
        for n in list(range(25))+[10**18-i for i in range(8)]+[10**9,10**9-1,2**53,2**53+1]:
            add(n)
    elif pid == "114A":
        for k in (2,3,10,31,46340,46341,2**31-1):
            value=k
            while value<=2**31-1:
                add(k,value)
                if value>2:
                    add(k,value-1)
                if value<2**31-1:
                    add(k,value+1)
                value*=k
    elif pid == "680B":
        add(1,1,0)
        add(1,1,1)
        for a in (1,50,51,100):
            for bits in ([0]*100,[1]*100,[i%2 for i in range(100)]):
                add(100,a,*bits)
        for _ in range(25):
            n=rng.randint(1,100)
            add(n,rng.randint(1,n),*[rng.randrange(2) for _ in range(n)])
    elif pid == "622A":
        for k in (1,2,3,10,1000,10**6,14142135):
            t=k*(k+1)//2
            for n in (t-1,t,t+1):
                if 1<=n<=10**14:
                    add(n)
        add(10**14)
        for _ in range(20):
            add(rng.randint(1,10**14))
    elif pid == "777A":
        for n in list(range(1,13))+list(range(2*10**9-5,2*10**9+1)):
            for x in range(3):
                add(n,x)
    elif pid == "479A":
        for values in itertools.product((1,2,9,10),repeat=3):
            add(*values)
    elif pid == "75A":
        for a,b in [(1,1),(9,1),(10,10),(101,102),(105,106),(10**9,10**9),(999999999,1),(100000001,999999999),(909090909,909090909)]:
            add(a,b)
        for _ in range(25):
            add(rng.randint(1,10**9),rng.randint(1,10**9))
    elif pid == "131A":
        cases=[s+"\n" for s in ["a","A","z","Z","HTTP","hELLO","Hello","cAPS","aB","AB","Ab","ab","A"*100,"a"+"Z"*99,"z"*100,"Z"*99+"a"]]
        cases += ["".join(rng.choice("aAzZ") for _ in range(n))+"\n" for n in (2,3,5,99,100)]
    elif pid == "17A":
        for n in (2,3,5,7,13,19,27,100,999,1000):
            for k in (0,1,2,10,1000):
                add(n,k)
    elif pid == "515A":
        for a,b in [(0,0),(1,0),(-1,1),(10**9,10**9),(-10**9,-10**9),(10**9,0),(1,1),(-2,3)]:
            distance=abs(a)+abs(b)
            for s in (max(1,distance-1),max(1,distance),max(1,distance+1),max(1,distance+2),2*10**9):
                if s<=2*10**9:
                    add(a,b,s)
    elif pid == "577A":
        for n,x in [(1,1),(1,2),(100000,10**9),(100000,1),(100000,999999937),(100000,100000),(100000,999980001),(10,100),(10,99),(10,101)]:
            add(n,x)
        for _ in range(20):
            add(rng.randint(1,10**5),rng.randint(1,10**9))
    elif pid == "58A":
        words=["h","hello","hlelo","helllo","helol","hell","hello"+"a"*95,"a"*95+"hello","h"*96+"ello","h"*20+"e"*20+"l"*20+"l"*20+"o"*20,"a"*100,"hellohello"]
        words += ["".join(rng.choice("heloaz") for _ in range(n)) for n in (3,4,5,6,10,50,99,100)]
        cases=[w+"\n" for w in words]
    elif pid == "1036A":
        for n,k in [(1,1),(1,10**18),(10**18,1),(10**18,10**18),(999999999999999999,10**18),(2**53,2**53+1),(10**9,10**18),(3,10),(3,9),(3,8)]:
            add(n,k)
        for _ in range(20):
            add(rng.randint(1,10**18),rng.randint(1,10**18))
    elif pid == "124A":
        for n in (1,2,3,99,100):
            for a,b in itertools.product(sorted({0,n//2,n-1}),repeat=2):
                add(n,a,b)
    elif pid == "476A":
        for n in (1,2,3,4,9,10,11,9999,10000):
            for m in (2,3,9,10):
                add(n,m)
    elif pid == "859B":
        for k in (1,2,3,10,31,999,1000):
            for n in (k*k-1,k*k,k*k+1,k*(k+1)-1,k*(k+1),k*(k+1)+1):
                if 1<=n<=10**6:
                    add(n)
    elif pid == "659A":
        for n in (1,2,3,99,100):
            for a in sorted({1,n//2+1,n}):
                for b in (-100,-n,-1,0,1,n,100):
                    add(n,a,b)
    else:
        raise ValueError("unowned recipe")
    return list(dict.fromkeys(cases))


def extras(pid):
    return [{"input": layout(pid,text),"output":output(pid,text)} for text in extra_inputs(pid)]
