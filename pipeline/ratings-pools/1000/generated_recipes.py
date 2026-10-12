"""Generated-basis candidates; independent oracle/audit deliberately not fabricated."""
from collections import Counter
from bisect import bisect_left
import itertools
import random

from additional import REVIEW, array, flat, require, token, yn
from recipes import integers, within

IDS = tuple("29A 37A 69A 102B 127B 137B 165A 230A 237A 265B 284B 299A 339B 352A 359A 400A 404A 441A 447B 462A 465B 499A 499B 500A 560A 583A 608A 616B 641A 688B 691A 766B 886B 920A 967B 978C 981B 1008B".split())
RULES = {p: REVIEW[p]["input_format"]+" Unique token result under retained description; generated qualification and independent oracle/audit outstanding." for p in IDS}


def big_number(s,allow_zero):
    token(s,r"[0-9]+",1,100001)
    require((s=="0" and allow_zero) or (s[0]!="0" and (len(s)<=100000 or s=="1"+"0"*100000)))
    return s


def read_grid(v,n,m,low,high):
    array(v,n*m,low,high)
    return [v[i*m:(i+1)*m] for i in range(n)]


def output(pid,text):
    words = text.split()
    if pid in ("102B","688B"):
        require(len(words)==1)
        s = big_number(words[0],pid=="102B")
        if pid=="688B":
            return s+s[::-1]+"\n"
        operations = 0
        while len(s)>1:
            s = str(sum(map(int,s)))
            operations += 1
        return str(operations)+"\n"
    if pid in ("284B","404A","462A","641A","447B","400A","499B"):
        return string_output(pid,words)
    v = integers(text)
    if pid in ("37A","127B","137B","265B","299A","352A","465B","560A","691A","766B","886B"):
        n = v[0]
        limits = {"37A":(1,1000,1,1000),"127B":(1,100,1,100),"137B":(1,5000,1,5000),
                  "265B":(1,10**5,1,10**4),"299A":(1,10**5,1,10**9),"352A":(1,1000,0,5),
                  "465B":(1,1000,0,1),"560A":(1,1000,1,10**6),"691A":(1,1000,0,1),
                  "766B":(3,10**5,1,10**9),"886B":(1,2*10**5,0,2*10**5)}
        lo,hi,alo,ahi = limits[pid]
        within(n,lo,hi)
        a = array(v[1:],n,alo,ahi)
        counts = Counter(a)
        if pid=="37A":
            return f"{max(counts.values())} {len(counts)}\n"
        if pid=="127B":
            return str(sum(c//2 for c in counts.values())//2)+"\n"
        if pid=="137B":
            return str(n-len(set(x for x in a if x<=n)))+"\n"
        if pid=="265B":
            return str(a[0]+sum(abs(x-y) for x,y in zip(a,a[1:]))+2*n-1)+"\n"
        if pid=="299A":
            divisor = min(a)
            return str(divisor if all(x%divisor==0 for x in a) else -1)+"\n"
        if pid=="352A":
            require(all(x in (0,5) for x in a))
            if not counts[0]:
                return "-1\n"
            fives = counts[5]//9*9
            return ("5"*fives+"0"*counts[0] if fives else "0")+"\n"
        if pid=="465B":
            positions = [i for i,x in enumerate(a) if x]
            return str(0 if not positions else 1+sum(min(y-x,2) for x,y in zip(positions,positions[1:])))+"\n"
        if pid=="560A":
            require(len(counts)==n)
            return "-1\n" if 1 in counts else "1\n"
        if pid=="691A":
            return yn(a[0]==1 if n==1 else counts[0]==1)
        if pid=="766B":
            a = sorted(a)
            return yn(any(a[i]+a[i+1]>a[i+2] for i in range(n-2)))
        last = {x:i for i,x in enumerate(a)}
        return str(min(last,key=last.get))+"\n"
    if pid in ("29A","69A","165A","237A","1008B"):
        n = v[0]
        size = 3 if pid=="69A" else 2
        limit = 200 if pid=="165A" else 10**5 if pid in ("237A","1008B") else 100
        within(n,1,limit)
        require(len(v)==1+n*size)
        records = [v[1+i*size:1+(i+1)*size] for i in range(n)]
        if pid=="29A":
            for x,d in records:
                within(x,-10**4,10**4)
                within(abs(d),1,2*10**4)
            require(len({x for x,d in records})==n)
            spit = dict(records)
            return yn(any(x+d in spit and spit[x+d]==-d for x,d in records))
        if pid=="69A":
            array(v[1:],n*3,-100,100)
            return yn(all(sum(r[k] for r in records)==0 for k in range(3)))
        if pid=="165A":
            array(v[1:],n*2,-1000,1000)
            require(len(set(map(tuple,records)))==n)
            vertical,horizontal = {},{}
            for x,y in records:
                vertical.setdefault(x,[]).append(y)
                horizontal.setdefault(y,[]).append(x)
            count = sum(min(vertical[x])<y<max(vertical[x]) and min(horizontal[y])<x<max(horizontal[y]) for x,y in records)
            return str(count)+"\n"
        if pid=="237A":
            for h,m in records:
                within(h,0,23)
                within(m,0,59)
            times = [60*h+m for h,m in records]
            require(times==sorted(times))
            return str(max(Counter(times).values()))+"\n"
        height = 10**9
        for w,h in records:
            within(w,1,10**9)
            within(h,1,10**9)
            choices = [x for x in (w,h) if x<=height]
            if not choices:
                return "NO\n"
            height = max(choices)
        return "YES\n"
    if pid in ("230A","339B","500A","608A","499A"):
        require(len(v)>=2)
        first,n = v[:2]
        if pid=="230A":
            strength = first
            within(strength,1,10**4)
            within(n,1,1000)
            require(len(v)==2+2*n)
            dragons = [tuple(v[2+i*2:4+i*2]) for i in range(n)]
            for x,y in dragons:
                within(x,1,10**4)
                within(y,0,10**4)
            for x,y in sorted(dragons):
                if strength<=x:
                    return "NO\n"
                strength += y
            return "YES\n"
        if pid=="339B":
            houses,tasks = first,n
            within(houses,2,10**5)
            within(tasks,1,10**5)
            a = array(v[2:],tasks,1,houses)
            current,total = 1,0
            for target in a:
                total += (target-current)%houses
                current = target
            return str(total)+"\n"
        if pid=="500A":
            cells,target = first,n
            within(cells,3,30000)
            within(target,2,cells)
            require(len(v)==cells+1)
            jumps = v[2:]
            for i,x in enumerate(jumps,1):
                within(x,1,cells-i)
            current = 1
            while current<target:
                current += jumps[current-1]
            return yn(current==target)
        if pid=="608A":
            passengers,top = first,n
            within(passengers,1,100)
            within(top,1,1000)
            require(len(v)==2+2*passengers)
            records = [v[2+i*2:4+i*2] for i in range(passengers)]
            for floor,time in records:
                within(floor,1,top)
                within(time,1,1000)
            return str(max([top]+[floor+time for floor,time in records]))+"\n"
        moments,skip = first,n
        within(moments,1,50)
        within(skip,1,10**5)
        require(len(v)==2+2*moments)
        intervals = [v[2+i*2:4+i*2] for i in range(moments)]
        current,watch = 1,0
        for left,right in intervals:
            within(left,current,10**5)
            within(right,left,10**5)
            current += (left-current)//skip*skip
            watch += right-current+1
            current = right+1
        return str(watch)+"\n"
    if pid in ("359A","616B"):
        require(len(v)>=2)
        n,m = v[:2]
        within(n,3 if pid=="359A" else 1,50 if pid=="359A" else 100)
        within(m,3 if pid=="359A" else 1,50 if pid=="359A" else 100)
        grid = read_grid(v[2:],n,m,0 if pid=="359A" else 1,1 if pid=="359A" else 10**9)
        if pid=="616B":
            return str(max(map(min,grid)))+"\n"
        require(sum(map(sum,grid))>0 and all(grid[i][j]==0 for i in (0,n-1) for j in (0,m-1)))
        edge = any(grid[i][j] for i in range(n) for j in range(m) if i in (0,n-1) or j in (0,m-1))
        return "2\n" if edge else "4\n"
    if pid=="441A":
        n,budget = v[:2]
        within(n,1,50)
        within(budget,10**4,10**6)
        offset,buy = 2,[]
        for seller in range(1,n+1):
            require(offset<len(v))
            k = v[offset]
            within(k,1,50)
            prices = array(v[offset+1:offset+1+k],k,10**4,10**6)
            if min(prices)<budget:
                buy.append(seller)
            offset += k+1
        require(offset==len(v))
        return str(len(buy))+"\n"+" ".join(map(str,buy))+"\n"
    if pid=="583A":
        n = v[0]
        within(n,1,50)
        require(len(v)==1+2*n*n)
        pairs = [tuple(v[1+i*2:3+i*2]) for i in range(n*n)]
        require(len(set(pairs))==n*n)
        used_h,used_v,days = set(),set(),[]
        for day,(h,w) in enumerate(pairs,1):
            within(h,1,n)
            within(w,1,n)
            if h not in used_h and w not in used_v:
                used_h.add(h)
                used_v.add(w)
                days.append(day)
        return " ".join(map(str,days))+"\n"
    if pid=="920A":
        t = v[0]
        within(t,1,200)
        offset,total,answers = 1,0,[]
        for _ in range(t):
            require(offset+2<=len(v))
            n,k = v[offset:offset+2]
            within(n,1,200)
            within(k,1,n)
            taps = array(v[offset+2:offset+2+k],k,1,n)
            require(taps==sorted(set(taps)))
            total += n
            answers.append(max(min(abs(i-x) for x in taps) for i in range(1,n+1))+1)
            offset += 2+k
        require(offset==len(v) and total<=200)
        return "\n".join(map(str,answers))+"\n"
    if pid=="967B":
        n,a,b = v[:3]
        within(n,1,10**5)
        within(a,1,10**4)
        within(b,1,a)
        sizes = array(v[3:],n,1,10**4)
        total,blocked = sum(sizes),0
        for size in sorted(sizes[1:],reverse=True):
            if total*b<=a*sizes[0]:
                break
            total -= size
            blocked += 1
        return str(blocked)+"\n"
    if pid=="978C":
        n,m = v[:2]
        within(n,1,2*10**5)
        within(m,1,2*10**5)
        require(len(v)==2+n+m)
        rooms = array(v[2:2+n],n,1,10**10)
        cumulative = list(itertools.accumulate(rooms))
        queries = array(v[2+n:],m,1,cumulative[-1])
        require(queries==sorted(set(queries)))
        answers = []
        for q in queries:
            i = bisect_left(cumulative,q)
            answers.append(f"{i+1} {q-(cumulative[i-1] if i else 0)}")
        return "\n".join(answers)+"\n"
    if pid=="981B":
        offset,incomes = 0,{}
        for _ in range(2):
            require(offset<len(v))
            n = v[offset]
            within(n,1,10**5)
            require(offset+1+2*n<=len(v))
            seen = set()
            for i in range(n):
                idx,profit = v[offset+1+2*i:offset+3+2*i]
                within(idx,1,10**9)
                within(profit,1,10**9)
                require(idx not in seen)
                seen.add(idx)
                incomes[idx] = max(incomes.get(idx,0),profit)
            offset += 1+2*n
        require(offset==len(v))
        return str(sum(incomes.values()))+"\n"
    raise ValueError("unknown generated-basis recipe")


def string_output(pid,words):
    if pid=="447B":
        require(len(words)==28)
        s = token(words[0],r"[a-z]+",1,1000)
        k = int(words[1])
        within(k,0,1000)
        weights = array(integers(" ".join(words[2:])),26,0,1000)
        result = sum((i+1)*weights[ord(c)-97] for i,c in enumerate(s))
        result += max(weights)*k*(2*len(s)+k+1)//2
        return str(result)+"\n"
    if pid=="499B":
        require(len(words)>=2)
        n,m = map(int,words[:2])
        within(n,1,3000)
        within(m,1,3000)
        require(len(words)==2+2*m+n)
        first,second,mapping = set(),set(),{}
        for i in range(m):
            a,b = words[2+2*i:4+2*i]
            token(a,r"[a-z]+",1,10)
            token(b,r"[a-z]+",1,10)
            require(a not in first and b not in second)
            first.add(a)
            second.add(b)
            mapping[a] = a if len(a)<=len(b) else b
        require(not first.intersection(second))
        lecture = words[2+2*m:]
        require(all(c in mapping for c in lecture))
        return " ".join(mapping[c] for c in lecture)+"\n"
    require(words and words[0].isdigit())
    n = int(words[0])
    if pid=="400A":
        within(n,1,100)
        require(len(words)==n+1)
        answers = []
        for s in words[1:]:
            token(s,r"[XO]+",12,12)
            choices = [f"{a}x{12//a}" for a in (1,2,3,4,6,12) if any(all(s[row*(12//a)+col]=="X" for row in range(a)) for col in range(12//a))]
            answers.append(str(len(choices))+(" "+" ".join(choices) if choices else ""))
        return "\n".join(answers)+"\n"
    if pid=="284B":
        within(n,2,2*10**5)
        require(len(words)==2)
        s = token(words[1],r"[AIF]+",n,n)
        ins = s.count("I")
        return str(s.count("A") if ins==0 else 1 if ins==1 else 0)+"\n"
    if pid=="641A":
        within(n,1,10**5)
        require(len(words)==n+2)
        directions = token(words[1],r"[<>]+",n,n)
        distances = array(integers(" ".join(words[2:])),n,1,10**9)
        current,seen = 0,set()
        while 0<=current<n and current not in seen:
            seen.add(current)
            current += distances[current]*(1 if directions[current]==">" else -1)
        return "INFINITE\n" if current in seen else "FINITE\n"
    within(n,3 if pid=="404A" else 1,299 if pid=="404A" else 100)
    require(len(words)==n+1)
    grid = words[1:]
    for row in grid:
        token(row,r"[a-z]+" if pid=="404A" else r"[xo]+",n,n)
    if pid=="404A":
        require(n%2==1)
        diagonal,background = grid[0][0],grid[0][1]
        return yn(diagonal!=background and all(grid[i][j]==(diagonal if i==j or i+j==n-1 else background) for i in range(n) for j in range(n)))
    return yn(all(sum(grid[x][y]=="o" for x,y in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)) if 0<=x<n and 0<=y<n)%2==0 for i in range(n) for j in range(n)))


def lines(*rows):
    return "".join(flat(*row) if isinstance(row,(list,tuple)) else str(row)+"\n" for row in rows)


def values(n,lo,hi,mode,rng):
    return [lo if mode==-1 else hi if mode==-2 else lo if i%2 else hi if mode==-3 else rng.randint(lo,hi) for i in range(n)]


def make_input(pid,rng,mode):
    maximum = mode<0
    limits = {"37A":1000,"127B":100,"137B":5000,"265B":10**5,"299A":10**5,"352A":1000,
              "465B":1000,"560A":1000,"691A":1000,"766B":10**5,"886B":2*10**5}
    if pid in limits:
        n = limits[pid] if maximum else rng.randint(3 if pid=="766B" else 1,20)
        domains = {"37A":(1,1000),"127B":(1,100),"137B":(1,5000),"265B":(1,10**4),"299A":(1,10**9),"352A":(0,1),"465B":(0,1),"560A":(1,10**6),"691A":(0,1),"766B":(1,10**9),"886B":(0,2*10**5)}
        lo,hi = domains[pid]
        a = values(n,lo,hi,mode,rng)
        if pid=="352A":
            a = [5*x for x in a]
        if pid=="560A":
            a = list(range(1,n+1)) if mode==-1 else list(range(10**6-n+1,10**6+1)) if mode==-2 else rng.sample(range(1,10**6+1),n)
        return lines(n,a)
    if pid in ("102B","688B"):
        s = "1"+"0"*100000 if mode==-1 else "9"*100000 if mode==-2 else "1"+"01"*49999 if mode==-3 else str(rng.randint(0 if pid=="102B" else 1,10**9))
        return s+"\n"
    if pid in ("29A","69A","165A","237A","1008B"):
        limit = 200 if pid=="165A" else 10**5 if pid in ("237A","1008B") else 100
        n = limit if maximum else rng.randint(1,15)
        if pid=="29A":
            positions = rng.sample(range(-10**4,10**4+1),n)
            records = [(x,rng.choice([-1,1])*rng.randint(1,2*10**4)) for x in positions]
            if n>=2 and mode%2==0:
                records[0] = (positions[0],positions[1]-positions[0])
                records[1] = (positions[1],positions[0]-positions[1])
        elif pid=="69A":
            records = [values(3,-100,100,mode,rng) for _ in range(n)]
            if mode==-3:
                records = [[100,-100,0] if i%2 else [-100,100,0] for i in range(n)]
        elif pid=="165A":
            universe = [(x,y) for x in range(-20,21) for y in range(-20,21)]
            records = rng.sample(universe,n)
            if mode==-1:
                records = [(i-100,1000) for i in range(n)]
            if mode==-2:
                records = [(1000,i-100) for i in range(n)]
        elif pid=="237A":
            times = sorted(values(n,0,1439,mode,rng))
            records = [divmod(t,60) for t in times]
        else:
            records = [values(2,1,10**9,mode,rng) for _ in range(n)]
            if mode==-3:
                records = [(10**9-i,1+i) for i in range(n)]
        return lines(n,*records)
    if pid=="230A":
        n = 1000 if maximum else rng.randint(1,12)
        strength = 1 if mode==-1 else 10000 if mode==-2 else rng.randint(1,10000)
        dragons = [(rng.randint(1,10000),rng.randint(0,10000)) for _ in range(n)]
        if mode==-1:
            dragons = [(1,0)]*n
        if mode==-2:
            dragons = [(9999,10000)]*n
        return lines((strength,n),*dragons)
    if pid=="339B":
        n,m = (10**5,10**5) if maximum else (rng.randint(2,20),rng.randint(1,20))
        return lines((n,m),values(m,1,n,mode,rng))
    if pid=="284B":
        n = 2*10**5 if maximum else rng.randint(2,20)
        s = "A"*n if mode==-1 else "I"*n if mode==-2 else "I"+"A"*(n-1) if mode==-3 else "".join(rng.choice("AIF") for _ in range(n))
        return lines(n,s)
    if pid in ("359A","616B"):
        hi,lo = (50,3) if pid=="359A" else (100,1)
        n,m = (hi,hi) if maximum else (rng.randint(lo,8),rng.randint(lo,8))
        grid = [values(m,0 if pid=="359A" else 1,1 if pid=="359A" else 10**9,mode,rng) for _ in range(n)]
        if pid=="359A":
            for i in (0,n-1):
                for j in (0,m-1):
                    grid[i][j] = 0
            if mode==-1:
                grid[1][1] = 1
            if not any(map(any,grid)):
                grid[0][1] = 1
        return lines((n,m),*grid)
    if pid=="400A":
        t = 100 if maximum else rng.randint(1,12)
        rows = ["X"*12 if mode==-1 else "O"*12 if mode==-2 else "XO"*6 if mode==-3 else "".join(rng.choice("XO") for _ in range(12)) for _ in range(t)]
        return lines(t,*rows)
    if pid in ("404A","462A"):
        n = 299 if pid=="404A" and maximum else 100 if maximum else rng.choice([3,5,7,9]) if pid=="404A" else rng.randint(1,8)
        if pid=="404A":
            diagonal,background = rng.sample("abcdefghijklmnopqrstuvwxyz",2)
            grid = ["".join(diagonal if i==j or i+j==n-1 else background for j in range(n)) for i in range(n)]
            if mode%2==0:
                grid[0] = background+grid[0][1:]
        else:
            grid = ["x"*n if mode==-1 else "o"*n if mode==-2 else "".join(rng.choice("xo") for _ in range(n)) for _ in range(n)]
        return lines(n,*grid)
    if pid=="441A":
        n = 50 if maximum else rng.randint(1,8)
        budget = 10**4 if mode==-1 else 10**6 if mode==-2 else rng.randint(10**4,10**6)
        sellers = []
        for _ in range(n):
            k = 50 if maximum else rng.randint(1,8)
            sellers.append([k]+values(k,10**4,10**6,mode,rng))
        return lines((n,budget),*sellers)
    if pid=="447B":
        n,k = (1000,1000) if maximum else (rng.randint(1,20),rng.randint(0,20))
        s = "z"*n if mode==-1 else "a"*n if mode==-2 else "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
        return lines(s,k,values(26,0,1000,mode,rng))
    if pid=="499A":
        n = 50 if maximum else rng.randint(1,12)
        x = 10**5 if mode==-1 else 1 if mode==-2 else rng.randint(1,100)
        intervals,current = [],1
        for _ in range(n):
            left = current+rng.randint(0,20)
            right = left+rng.randint(0,20)
            intervals.append((left,right))
            current = right+1
        if maximum:
            intervals[-1] = (99999,100000)
        return lines((n,x),*intervals)
    if pid=="499B":
        n,m = (3000,3000) if maximum else (rng.randint(1,20),rng.randint(1,20))
        def encode(i):
            s = ""
            while i:
                i,r = divmod(i,26)
                s += chr(97+r)
            return s or "a"
        pairs = [("a"+encode(i),"z"+encode(i)+("zz" if i%2 else "")) for i in range(m)]
        return lines((n,m),*pairs,[rng.choice(pairs)[0] for _ in range(n)])
    if pid=="500A":
        n = 30000 if maximum else rng.randint(3,25)
        target = n if maximum else rng.randint(2,n)
        jumps = [1 if mode==-1 else n-i if mode==-2 else rng.randint(1,n-i) for i in range(1,n)]
        return lines((n,target),jumps)
    if pid=="583A":
        n = 50 if maximum else rng.randint(1,10)
        schedule = [(h,w) for h in range(1,n+1) for w in range(1,n+1)]
        if mode==-2:
            schedule.reverse()
        elif mode!=-1:
            rng.shuffle(schedule)
        return lines(n,*schedule)
    if pid=="608A":
        n,s = (100,1000) if maximum else (rng.randint(1,12),rng.randint(1,30))
        records = [(1 if mode==-1 else s if mode==-2 else rng.randint(1,s),1000 if maximum else rng.randint(1,100)) for _ in range(n)]
        return lines((n,s),*records)
    if pid=="641A":
        n = 10**5 if maximum else rng.randint(1,25)
        directions = "<"*n if mode==-1 else "><"+">"*(n-2) if mode==-2 else "".join(rng.choice("<>") for _ in range(n))
        distances = [1]*n if mode==-2 else values(n,1,10**9,mode,rng)
        return lines(n,directions,distances)
    if pid=="920A":
        if mode==-3:
            return lines(200,*[row for _ in range(200) for row in ((1,1),(1,))])
        n = 200 if maximum else rng.randint(1,20)
        taps = [1] if mode==-1 else [200] if mode==-2 else list(range(1,201)) if mode==-3 else sorted(rng.sample(range(1,n+1),rng.randint(1,n)))
        return lines(1,(n,len(taps)),taps)
    if pid=="967B":
        n = 10**5 if maximum else rng.randint(1,20)
        a = 10000 if maximum else rng.randint(1,20)
        b = a if mode==-1 else 1 if mode==-2 else rng.randint(1,a)
        return lines((n,a,b),values(n,1,10000,mode,rng))
    if pid=="978C":
        n,m = (2*10**5,2*10**5) if maximum else (rng.randint(1,15),rng.randint(1,15))
        if mode==-2:
            m = 1
        if mode==-3:
            n,m = 1,1
        rooms = [1 if mode==-1 else 10**10]*n if maximum else [rng.randint(1,30) for _ in range(n)]
        m = min(m,sum(rooms))
        queries = list(range(1,m+1)) if mode==-1 else list(range(sum(rooms)-m+1,sum(rooms)+1)) if mode==-2 else sorted(rng.sample(range(1,sum(rooms)+1),m))
        return lines((n,m),rooms,queries)
    if pid=="981B":
        n,m = (10**5,10**5) if maximum else (rng.randint(1,12),rng.randint(1,12))
        if mode==-3:
            return lines(1,(10**9,10**9),1,(10**9,1))
        first = [(i+1,1 if mode==-1 else 10**9 if maximum else rng.randint(1,100)) for i in range(n)]
        second = [(i+1+(10**8 if mode==-2 else 0),1 if mode==-1 else 10**9 if maximum else rng.randint(1,100)) for i in range(m)]
        return lines(n,*first,m,*second)
    raise ValueError("unimplemented generated input")


def extras(pid):
    rng = random.Random("1000-generated-v1-"+pid)
    seen,result = set(),[]
    for mode in [-1,-2,-3]+list(range(180)):
        text = make_input(pid,rng,mode)
        if text in seen:
            continue
        seen.add(text)
        result.append({"input":text,"output":output(pid,text),"caseKind":"max-size" if mode<0 else "boundary-adversarial"})
    return result
