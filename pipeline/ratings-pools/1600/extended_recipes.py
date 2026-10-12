"""Additional exact token-answer recipes with independent bounded brute checks."""
from collections import Counter, deque
import itertools
import math
import random

IDS = ('165C', '383A', '348A', '1025C', '1062C', '1398C', '1458A', '1334C', '1251C')
MOD = 10**9 + 7
SEMANTICS = {
    '165C': 'Count substring occurrences with exactly k ones, including k0. k0..10^6; binary length1..10^6. Prefix-one count frequencies give all endpoints; exhaustive small substrings independently checked.',
    '383A': 'Minimum total lost milk is number of right-facing cows before left-facing cows; each opposing pair inevitably loses one unit. n1..200000, bits0/1; exhaustive milking orders on short rows checked.',
    '348A': 'Minimum Mafia rounds max(max(a),ceil(sum(a)/(n-1))). n3..100000, demands1..10^9; each person can supervise at most rounds-a_i rounds and total supervisory capacity must cover all rounds. Small supervisor assignments independently checked.',
    '1025C': 'Maximum alternating zebra length under reversing both cut parts. Binary b/w length1..100000; operation produces dihedral transformations of cyclic sequence. Longest circular alternating run capped at n; exhaustive reachable states independently checked.',
    '1062C': 'Unique per-range maximum enjoyment modulo10^9+7: (2^ones-1)*2^zeros. n,q1..100000; exact length and l<=r bounds. All eating orders on short bitstrings independently simulated.',
    '1398C': 'Count good subarrays: prefix of digit-minus-one equal at both ends. t1..1000, n1..100000,totaln<=100000; decimal digits exact length. All short subarray sums independently checked.',
    '1458A': 'Per b_j GCD equals gcd(a_1+b_j,gcd(a_i-a_1)). n,m1..200000; positive entries<=10^18. Equal a values permit gcd-of-differences zero. Small direct GCD checks independent of reduction.',
    '1334C': 'Circle monsters: sum of max(0,a_i-b_previous) plus min_i min(a_i,b_previous). T1..150000,n2..300000,totaln<=300000,a/b1..10^12. Small shortest-bullet BFS with cascading explosions independently checked.',
    '1251C': 'Lexicographically smallest stable merge of even and odd subsequences, preserving leading zeros. t1..10000,length1..300000,total length<=300000,decimal digits. Adjacent cross-parity swap closure independently enumerated on short strings.',
}


def parse(pid, text):
    v = text.split()
    if pid in ('165C', '1025C'):
        if pid == '165C' and len(v) == 2 and 0 <= int(v[0]) <= 10**6 and 1 <= len(v[1]) <= 10**6 and not set(v[1]) - set('01'):
            return int(v[0]), v[1]
        if pid == '1025C' and len(v) == 1 and 1 <= len(v[0]) <= 10**5 and not set(v[0]) - set('bw'):
            return v[0]
        raise ValueError('string arity/alphabet/range')
    if pid in ('383A', '348A'):
        a = list(map(int, v)); n = a[0]
        if len(a) != n + 1 or not (1 if pid == '383A' else 3) <= n <= (200000 if pid == '383A' else 100000):
            raise ValueError('array arity/size')
        if not all(0 <= x <= 1 if pid == '383A' else 1 <= x <= 10**9 for x in a[1:]):
            raise ValueError('array values')
        return a[1:]
    if pid == '1458A':
        a = list(map(int, v)); n, m = a[:2]
        if not 1 <= n <= 200000 or not 1 <= m <= 200000 or len(a) != n + m + 2 or not all(1 <= x <= 10**18 for x in a[2:]):
            raise ValueError('GCD dimensions/arity/ranges')
        return a[2:2+n], a[2+n:]
    if pid == '1062C':
        n, q = map(int, v[:2]); s = v[2]
        if not 1 <= n <= 100000 or not 1 <= q <= 100000 or len(s) != n or set(s) - set('01') or len(v) != 3 + 2*q:
            raise ValueError('Banh-mi dimensions/length/arity')
        queries = list(zip(map(int, v[3::2]), map(int, v[4::2])))
        if not all(1 <= l <= r <= n for l, r in queries):
            raise ValueError('Banh-mi query range')
        return s, queries
    t = int(v[0]); i, total, cases = 1, 0, []
    if not 1 <= t <= {'1398C':1000, '1334C':150000, '1251C':10000}[pid]:
        raise ValueError('test count')
    for _ in range(t):
        if pid == '1251C':
            s = v[i]; i += 1; n = len(s)
            if not 1 <= n <= 300000 or set(s) - set('0123456789'):
                raise ValueError('decimal length/alphabet')
            cases.append(s)
        elif pid == '1398C':
            n, s = int(v[i]), v[i+1]; i += 2
            if not 1 <= n <= 100000 or len(s) != n or set(s) - set('0123456789'):
                raise ValueError('good-subarray length/alphabet')
            cases.append(s)
        else:
            n = int(v[i]); i += 1
            vals = list(map(int, v[i:i+2*n])); i += 2*n
            if not 2 <= n <= 300000 or len(vals) != 2*n or not all(1 <= x <= 10**12 for x in vals):
                raise ValueError('monster dimensions/ranges')
            cases.append(list(zip(vals[::2], vals[1::2])))
        total += n
    if i != len(v) or total > (100000 if pid == '1398C' else 300000):
        raise ValueError('global size/arity')
    return cases


def zebra(s):
    best = run = 1
    for x, y in zip(s+s, (s+s)[1:]):
        run = run + 1 if x != y else 1
        best = max(best, run)
    return min(len(s), best)


def merge_parity(s):
    even, odd = [c for c in s if int(c)%2 == 0], [c for c in s if int(c)%2]
    out, i, j = [], 0, 0
    while i < len(even) and j < len(odd):
        if even[i] < odd[j]:
            out.append(even[i]); i += 1
        else:
            out.append(odd[j]); j += 1
    return ''.join(out + even[i:] + odd[j:])


def good(s):
    freq, prefix, result = Counter({0:1}), 0, 0
    for c in s:
        prefix += int(c)-1; result += freq[prefix]; freq[prefix] += 1
    return result


def monsters(values):
    required = [max(0, a-values[(i-1)%len(values)][1]) for i,(a,_) in enumerate(values)]
    return sum(required) + min(a-r for (a,_),r in zip(values,required))


def answer(pid, data):
    if pid == '165C':
        k,s = data; counts, pref, total = Counter({0:1}), 0, 0
        for c in s:
            pref += int(c); total += counts[pref-k]; counts[pref] += 1
        return [total]
    if pid == '383A':
        right = total = 0
        for x in data:
            if x: right += 1
            else: total += right
        return [total]
    if pid == '348A': return [max(max(data), (sum(data)+len(data)-2)//(len(data)-1))]
    if pid == '1025C': return [zebra(data)]
    if pid == '1458A':
        a,b = data; g = 0
        for x in a: g = math.gcd(g,x-a[0])
        return [math.gcd(g,a[0]+x) for x in b]
    if pid == '1062C':
        s,queries = data; prefix = [0]; powers = [1]
        for c in s:
            prefix.append(prefix[-1]+int(c)); powers.append(powers[-1]*2%MOD)
        return [(powers[prefix[r]-prefix[l-1]]-1)*powers[r-l+1-prefix[r]+prefix[l-1]]%MOD for l,r in queries]
    if pid == '1398C': return [good(s) for s in data]
    if pid == '1334C': return [monsters(v) for v in data]
    return [merge_parity(s) for s in data]


def closure(s, moves):
    seen, queue = {s}, deque([s])
    while queue:
        for v in moves(queue.popleft()):
            if v not in seen: seen.add(v); queue.append(v)
    return seen


def brute_monsters(values):
    start = tuple(a for a,b in values); blasts = [b for a,b in values]
    queue, seen = deque([(start,0)]), {start}
    while queue:
        state,cost = queue.popleft()
        if not any(state): return cost
        for i,h in enumerate(state):
            if not h: continue
            nxt = list(state); nxt[i] -= 1; j=i
            while nxt[j] == 0:
                target = (j+1)%len(state)
                if nxt[target] == 0: break
                nxt[target] = max(0,nxt[target]-blasts[j]); j=target
            nxt = tuple(nxt)
            if nxt not in seen: seen.add(nxt); queue.append((nxt,cost+1))


def brute_checks():
    counts = Counter(); rng = random.Random(160019)
    for n in range(1,7):
        for bits in itertools.product('01',repeat=n):
            s=''.join(bits)
            for k in range(n+2):
                expect=sum(s[i:j].count('1')==k for i in range(n) for j in range(i+1,n+1))
                assert answer('165C',(k,s))==[expect]; counts['165C']+=1
            expected=min(sum(1 for pos,i in enumerate(order) for j in order[pos+1:]
                             if (j<i and bits[j]=='1') or (j>i and bits[j]=='0')) for order in itertools.permutations(range(n)))
            assert answer('383A',list(map(int,bits)))==[expected]; counts['383A']+=1
            enjoy=[]
            for order in itertools.permutations(range(n)):
                v=list(map(int,bits)); total=0
                for i in order:
                    x=v[i]; total+=x
                    for j in range(n):
                        if j not in order[:order.index(i)+1]: v[j]+=x
                enjoy.append(total)
            assert answer('1062C',(s,[(1,n)]))==[max(enjoy)]; counts['1062C']+=1
    for n in range(1,8):
        for bits in itertools.product('bw',repeat=n):
            s=''.join(bits)
            reachable=closure(s,lambda v: [v[:i][::-1]+v[i:][::-1] for i in range(1,len(v))])
            expected=max(max((j-i for i in range(n) for j in range(i+1,n+1) if all(v[k]!=v[k+1] for k in range(i,j-1))),default=1) for v in reachable)
            assert zebra(s)==expected; counts['1025C']+=1
    for demands in itertools.product(range(1,4),repeat=3):
        expected=None
        for rounds in range(1,7):
            if any(all(rounds-order.count(i)>=demands[i] for i in range(3)) for order in itertools.product(range(3),repeat=rounds)):
                expected=rounds;break
        assert answer('348A',demands)==[expected]; counts['348A']+=1
    for n in range(1,6):
        for digits in itertools.product('0123',repeat=n):
            s=''.join(digits); expected=sum(sum(map(int,s[i:j]))==j-i for i in range(n) for j in range(i+1,n+1))
            assert good(s)==expected;counts['1398C']+=1
    for _ in range(100):
        a=[rng.randint(1,1000) for _ in range(rng.randint(1,8))]; b=[rng.randint(1,1000) for _ in range(8)]
        assert answer('1458A',(a,b))==[math.gcd(*(v+x for v in a)) for x in b]; counts['1458A']+=1
        vals=[(rng.randint(1,4),rng.randint(1,4)) for _ in range(rng.randint(2,4))]
        assert monsters(vals)==brute_monsters(vals); counts['1334C']+=1
    for digits in itertools.product('0123',repeat=4):
        s=''.join(digits)
        reachable=closure(s,lambda v: [v[:i]+v[i+1]+v[i]+v[i+2:] for i in range(len(v)-1) if int(v[i])%2!=int(v[i+1])%2])
        assert merge_parity(s)==min(reachable); counts['1251C']+=1
    return dict(counts)


def extras(pid):
    rng=random.Random(160000+int(pid[:-1])); cases=[]
    def add(text,reason,category='adversarial'):
        cases.append({'input':text,'output':'\n'.join(map(str,answer(pid,parse(pid,text))))+'\n','reason':reason,'category':category})
    def arr(a): return str(len(a))+'\n'+' '.join(map(str,a))+'\n'
    if pid=='165C':
        for k,s in [(0,'0'),(0,'1'),(1,'1'),(2,'1'),(0,'000000'),(1,'0010001000'),(10**6,'1'*10**6),(0,'0'*10**6)]:
            add(f'{k}\n{s}\n','zero ones, excess budget, long zero gaps,64-bit counts','maxSize' if len(s)==10**6 else 'boundary')
        for _ in range(50):
            s=''.join(rng.choice('01') for _ in range(rng.randint(1,200))); add(f'{rng.randint(0,len(s)+2)}\n{s}\n','fixed-seed binary substrings')
    elif pid in ('383A','348A'):
        fixed=([0],[1],[1,0],[0,1],[1,1,0,0],[0]*200000,[1]*100000+[0]*100000) if pid=='383A' else ([1,1,1],[1,2,100],[3,3,3],[10**9]*100000)
        for a in fixed: add(arr(a),'minimum, homogeneous, opposing runs/uneven demands','maxSize' if len(a)>100 else 'boundary')
        for _ in range(40):
            a=[rng.randint(0,1) if pid=='383A' else rng.randint(1,10**9) for _ in range(rng.randint(1 if pid=='383A' else 3,100))]; add(arr(a),'fixed-seed adversarial row/demand distribution')
    elif pid=='1025C':
        for s in ['b','w','bb','bw','bwb','bbwbw','b'*100000,'bw'*50000]:
            add(s+'\n','single stripe, cyclic wrap, uniform/full alternating','maxSize' if len(s)==100000 else 'boundary')
        for _ in range(40): add(''.join(rng.choice('bw') for _ in range(rng.randint(1,100)))+'\n','fixed-seed circular alternating runs')
    elif pid=='1062C':
        for s in ['0','1','01010','000000','111111']:
            q=[(i,j) for i in range(1,len(s)+1) for j in range(i,len(s)+1)]
            add(f'{len(s)} {len(q)}\n{s}\n'+''.join(f'{l} {r}\n' for l,r in q),'all subranges including singleton/zero/full-ones','boundary')
        s='10'*50000;q=[(1,100000)]*100000
        add('100000 100000\n'+s+'\n'+''.join(f'{l} {r}\n' for l,r in q),'maximal n/q, modular powers and output size','maxSize')
        for _ in range(15):
            n=rng.randint(1,200);s=''.join(rng.choice('01') for _ in range(n));q=[]
            for __ in range(40):
                l=rng.randint(1,n);q.append((l,rng.randint(l,n)))
            add(f'{n} {len(q)}\n{s}\n'+''.join(f'{l} {r}\n' for l,r in q),'fixed-seed repeated/overlapping ranges')
    elif pid=='1398C':
        for s in ['0','1','9','120','0'*100000,'1'*100000,'9'*100000]:
            add('1\n'+str(len(s))+'\n'+s+'\n','zero/single/mixed digits and64-bit all-one count','maxSize' if len(s)==100000 else 'boundary')
        add('1000\n'+('1\n1\n'*1000),'maximum test case count','boundary')
        for _ in range(15):
            values=[''.join(rng.choice('0123456789') for __ in range(rng.randint(1,100))) for ___ in range(40)]
            add('40\n'+''.join(f'{len(s)}\n{s}\n' for s in values),'fixed-seed decimal subarrays')
    elif pid=='1458A':
        for a,b in [([1],[1]),([10**18],[10**18]),([7,7,7],[1,7,10**18]),([6,10,14],[2,3,4]),([10**18]*200000,[10**18]*200000)]:
            add(f'{len(a)} {len(b)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n','zero differences, singleton, large sums','maxSize' if len(a)==200000 else 'boundary')
        for _ in range(20):
            a=[rng.randint(1,10**18) for _ in range(rng.randint(1,60))];b=[rng.randint(1,10**18) for _ in range(40)]
            add(f'{len(a)} {len(b)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n','fixed-seed common-divisor range')
    elif pid=='1334C':
        for values in [[(1,1),(1,1)],[(10**12,1),(10**12,1)],[(1,10**12),(10**12,1)],[(10**12,1)]*300000]:
            add('1\n'+str(len(values))+'\n'+''.join(f'{a} {b}\n' for a,b in values),'chain explosions, wrap-around,64-bit bullet sum','maxSize' if len(values)==300000 else 'boundary')
        add('150000\n'+('2\n1 1\n1 1\n'*150000),'maximal case count at total monster budget','maxSize')
        for _ in range(15):
            groups=[[(rng.randint(1,1000),rng.randint(1,1000)) for __ in range(rng.randint(2,20))] for ___ in range(30)]
            add('30\n'+''.join(str(len(g))+'\n'+''.join(f'{a} {b}\n' for a,b in g) for g in groups),'fixed-seed cascade/starting-monster choices')
    else:
        for s in ['0','9','032867235','9753108642','0'*300000,'98'*150000]:
            add('1\n'+s+'\n','leading zeros, mixed/single parity, maximal stable merge','maxSize' if len(s)==300000 else 'boundary')
        add('10000\n'+('0\n'*10000),'maximum test case count','boundary')
        for _ in range(15):
            values=[''.join(rng.choice('0123456789') for __ in range(rng.randint(1,100))) for ___ in range(40)]
            add('40\n'+'\n'.join(values)+'\n','fixed-seed reachable parity merges')
    return cases


def review(pid,tests,samples):
    failures=[]
    for name,pair in [*tests,*samples]:
        try:
            expected=list(map(str,answer(pid,parse(pid,pair['input']))))
            if pair['output'].split()!=expected: raise ValueError('output differs from independent oracle')
        except (ValueError,IndexError,KeyError,AssertionError) as exc:
            failures.append({'test':name,'reason':str(exc)})
    return failures
