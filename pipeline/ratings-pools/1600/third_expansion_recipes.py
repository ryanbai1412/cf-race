"""Exact yes/no oracles with independent bounded searches and legal maximum cases."""
from collections import Counter
import itertools
import math
import random

IDS = ('952C', '825B', '922C')
SEMANTICS = {
    '952C': 'n1..10, values1..100. Every neighboring pair must differ by at most1. Removing a maximum preserves that invariant; independent leftmost-maximum simulation checks each stage. The optional ravioli illustration is not needed for the fully stated rule.',
    '825B': 'Exactly10x10 cells X/O/dot; equal positive X and O counts, at least one empty, neither player initially wins. Unique yes/no asks whether one empty placement creates at least five consecutive X in any of four directions. Independent placement-and-scan brute checked.',
    '922C': 'n,k1..10^18. Distinct remainders necessarily equal0..k-1 in order, so every i1..k divides n+1. Incremental LCM stops once it exceeds n+1; exhaustive direct remainder-set checks bounded n,k. Case-insensitive yes/no token comparison is appropriate.',
}


def lines(board, mark):
    for r in range(10):
        for c in range(10):
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                endr,endc = r+4*dr,c+4*dc
                if 0 <= endr < 10 and 0 <= endc < 10:
                    yield [board[r+i*dr][c+i*dc] for i in range(5)]


def has_win(board,mark):
    return any(all(cell == mark for cell in window) for window in lines(board,mark))


def parse(pid,text):
    if pid == '825B':
        board = text.split()
        counts = Counter(''.join(board))
        if (len(board) != 10 or any(len(row) != 10 for row in board)
                or set(counts)-set('XO.') or counts['X'] != counts['O']
                or not counts['X'] or not counts['.'] or has_win(board,'X') or has_win(board,'O')):
            raise ValueError('board shape, balance, availability or initial win')
        return board
    a = list(map(int,text.split()))
    if pid == '952C':
        if not a or not 1 <= a[0] <= 10 or len(a) != a[0]+1 or not all(1 <= x <= 100 for x in a[1:]):
            raise ValueError('stack count/height/arity')
        return a[1:]
    if len(a) != 2 or not all(1 <= x <= 10**18 for x in a):
        raise ValueError('number/budget range or arity')
    return a


def answer(pid,data):
    if pid == '952C':
        yes = all(abs(a-b) <= 1 for a,b in zip(data,data[1:]))
    elif pid == '825B':
        yes = any(window.count('X') == 4 and window.count('.') == 1 for window in lines(data,'X'))
    else:
        n,k = data
        lcm,yes = 1,True
        for i in range(1,min(k,43)+1):
            lcm = math.lcm(lcm,i)
            if lcm > n+1 or (n+1)%lcm:
                yes = False
                break
    return ['YES' if yes else 'NO']


def brute(pid,data):
    if pid == '952C':
        remaining = list(data)
        extracted = []
        while remaining:
            if any(abs(a-b) >= 2 for a,b in zip(remaining,remaining[1:])):
                return ['NO']
            i = remaining.index(max(remaining))
            extracted.append(remaining.pop(i))
        return ['YES' if extracted == sorted(data,reverse=True) else 'NO']
    if pid == '922C':
        n,k = data
        return ['YES' if len({n%i for i in range(1,k+1)}) == k else 'NO']
    for r in range(10):
        for c in range(10):
            if data[r][c] != '.':
                continue
            board = [list(row) for row in data]
            board[r][c] = 'X'
            for sr in range(10):
                for sc in range(10):
                    for dr,dc in ((-1,0),(0,-1),(-1,-1),(-1,1)):
                        length,rr,cc = 0,sr,sc
                        while 0 <= rr < 10 and 0 <= cc < 10 and board[rr][cc] == 'X':
                            length += 1
                            rr,cc = rr+dr,cc+dc
                        if length >= 5:
                            return ['YES']
    return ['NO']


def extras(pid):
    rng = random.Random(160000+int(pid[:-1]))
    cases = []
    def add(data,reason,category='adversarial'):
        if pid == '952C':
            text = str(len(data))+'\n'+' '.join(map(str,data))+'\n'
        elif pid == '825B':
            text = '\n'.join(data)+'\n'
        else:
            text = ' '.join(map(str,data))+'\n'
        cases.append({'input':text,'output':answer(pid,parse(pid,text))[0]+'\n','reason':reason,'category':category})
    if pid == '952C':
        for data in ([1],[100],[1,2,3],[3,1,2],[1,2,3,2,1],[100,99,98,97,96,95,94,93,92,91],[1]*10,[100]*10,[1,100]*5):
            add(data,'singletons, unequal neighbors, smooth broad range or tallest tie','boundary' if len(data)<10 else 'maxSize')
        for _ in range(150):
            n = rng.randint(1,10)
            data = [rng.randint(1,100)]
            for _ in range(n-1):
                data.append(max(1,min(100,data[-1]+rng.choice((-2,-1,0,1,2)))))
            add(data,'fixed-seed near-invariant stacks')
    elif pid == '922C':
        for data in ((1,1),(1,2),(1,3),(5,3),(4,4),(10**18,1),(10**18,10**18),(10**18,42),(10**18,43)):
            add(data,'minimum, singleton remainder, maximum or LCM cutoff','maxSize' if max(data)==10**18 else 'boundary')
        lcm = 1
        for k in range(2,43):
            lcm = math.lcm(lcm,k)
            for offset in (-1,0,1):
                n = lcm+offset
                if 1 <= n <= 10**18:
                    add((n,k),'LCM divisibility transition')
        for _ in range(150):
            add((rng.randint(1,10**18),rng.randint(1,60)),'fixed-seed large remainder collisions')
    else:
        for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
            for missing in range(5):
                board = [['.']*10 for _ in range(10)]
                for i in range(5):
                    if i != missing:
                        board[1+i*dr][5+i*dc] = 'X'
                for r,c in ((8,0),(8,2),(8,4),(8,6)):
                    board[r][c] = 'O'
                add([''.join(row) for row in board],'each direction and each missing position','boundary')
        for count in [1,49]+[rng.randint(1,49) for _ in range(140)]:
            while True:
                positions = rng.sample(range(100),2*count)
                board = [['.']*10 for _ in range(10)]
                for i,p in enumerate(positions):
                    board[p//10][p%10] = 'X' if i<count else 'O'
                rows = [''.join(row) for row in board]
                if not has_win(rows,'X') and not has_win(rows,'O'):
                    break
            add(rows,'balanced legal board with sparse or dense occupancy','maxSize' if count==49 else 'adversarial')
    return cases


def brute_checks():
    counts = Counter()
    def check(pid,data):
        assert answer(pid,data) == brute(pid,data), (pid,data)
        counts[pid] += 1
    for n in range(1,8):
        for data in itertools.product(range(1,5),repeat=n):
            check('952C',data)
    for n in range(1,501):
        for k in range(1,81):
            check('922C',(n,k))
    for case in extras('825B'):
        check('825B',parse('825B',case['input']))
    return dict(counts)


def review(pid,tests,samples):
    failures = []
    for name,pair in [*tests,*samples]:
        try:
            if [x.upper() for x in pair['output'].split()] != answer(pid,parse(pid,pair['input'])):
                raise ValueError('oracle output differs from supplied bytes')
        except (ValueError,IndexError,KeyError,TypeError) as exc:
            failures.append({'test':name,'reason':str(exc)})
    return failures
