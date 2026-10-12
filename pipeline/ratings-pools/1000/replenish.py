"""Statement-reviewed replenishment; no independent audit signoff implied."""
from collections import Counter
import math
import random

from additional import REVIEW,array,require,token,yn
from generated_recipes import lines,values
from recipes import integers,within

IDS = tuple("336A 727A 14B 43A 56A 74A 106B 182B 637A 670B 672B 699A 725A 757A 844A".split())
RULES = {p:REVIEW[p]["input_format"]+" Unique result under retained statement; 727A inverse operations have disjoint parity and determine one path. Independent audit required." for p in IDS}
DRINKS = "ABSINTH BEER BRANDY CHAMPAGNE GIN RUM SAKE TEQUILA VODKA WHISKEY WINE".split()


def output(pid,text):
    w = text.split()
    require(bool(w))
    if pid in ("43A","56A","74A","672B","699A","725A","757A","844A"):
        return string_output(pid,w)
    v = integers(text)
    if pid=="336A":
        require(len(v)==2)
        x,y = v
        within(x,-10**9,10**9)
        within(y,-10**9,10**9)
        require(x!=0 and y!=0)
        distance = abs(x)+abs(y)
        points = sorted([(distance if x>0 else -distance,0),(0,distance if y>0 else -distance)])
        return " ".join(map(str,points[0]+points[1]))+"\n"
    if pid=="727A":
        require(len(v)==2)
        a,b = v
        within(a,1,10**9-1)
        within(b,a+1,10**9)
        sequence,current = [b],b
        while current>a:
            if current%2==0:
                current //= 2
            elif current%10==1:
                current //= 10
            else:
                return "NO\n"
            sequence.append(current)
        return "NO\n" if current!=a else "YES\n"+str(len(sequence))+"\n"+" ".join(map(str,sequence[::-1]))+"\n"
    if pid=="14B":
        n,x = v[:2]
        within(n,1,100)
        within(x,0,1000)
        require(len(v)==2+2*n)
        low,high = 0,1000
        for i in range(n):
            a,b = v[2+i*2:4+i*2]
            within(a,0,1000)
            within(b,0,1000)
            require(a!=b)
            low,high = max(low,min(a,b)),min(high,max(a,b))
        return str(-1 if low>high else max(0,low-x,x-high))+"\n"
    if pid=="106B":
        n = v[0]
        within(n,1,100)
        require(len(v)==1+4*n)
        laptops = [v[1+i*4:5+i*4] for i in range(n)]
        for s,r,h,c in laptops:
            within(s,1000,4200)
            within(r,256,4096)
            within(h,1,500)
            within(c,100,1000)
        require(len({row[3] for row in laptops})==n)
        eligible = [i for i,a in enumerate(laptops) if not any(all(b[k]>a[k] for k in range(3)) for b in laptops)]
        return str(min(eligible,key=lambda i:laptops[i][3])+1)+"\n"
    if pid=="182B":
        d,n = v[:2]
        within(d,1,10**6)
        within(n,1,2000)
        a = array(v[2:],n,1,d)
        return str(sum(d-x for x in a[:-1]))+"\n"
    if pid=="637A":
        n = v[0]
        within(n,1,1000)
        a = array(v[1:],n,1,10**6)
        final = Counter(a)
        maximum = max(final.values())
        running = Counter()
        for x in a:
            running[x] += 1
            if running[x]==maximum:
                return str(x)+"\n"
    if pid=="670B":
        n,k = v[:2]
        within(n,1,10**5)
        within(k,1,min(2*10**9,n*(n+1)//2))
        a = array(v[2:],n,1,10**9)
        require(len(set(a))==n)
        row = (math.isqrt(8*k+1)-1)//2
        if row*(row+1)//2<k:
            row += 1
        index = k-row*(row-1)//2-1
        return str(a[index])+"\n"
    raise ValueError("unknown replenishment recipe")


def string_output(pid,w):
    if pid=="757A":
        require(len(w)==1)
        counts = Counter(token(w[0],r"[a-zA-Z]+",1,10**5))
        return str(min(counts[c]//n for c,n in Counter("Bulbasaur").items()))+"\n"
    if pid=="844A":
        require(len(w)==2)
        s = token(w[0],r"[a-z]+",1,1000)
        k = int(w[1])
        within(k,1,26)
        return "impossible\n" if len(s)<k else str(max(0,k-len(set(s))))+"\n"
    n = int(w[0])
    if pid in ("43A","56A"):
        within(n,1,100)
        require(len(w)==n+1)
        if pid=="43A":
            counts = Counter(token(s,r"[A-Z]+",1,10) for s in w[1:])
            require(len(counts)<=2 and sum(c==max(counts.values()) for c in counts.values())==1)
            return max(counts,key=counts.get)+"\n"
        checks = 0
        for s in w[1:]:
            if s.isascii() and s.isdigit():
                within(int(s),0,1000)
                checks += int(s)<18
            else:
                token(s,r"[A-Z]+",1,100)
                checks += s in DRINKS
        return str(checks)+"\n"
    if pid=="74A":
        within(n,1,50)
        require(len(w)==1+8*n)
        scores = {}
        for i in range(n):
            name,*nums = w[1+i*8:9+i*8]
            token(name,r"[a-zA-Z0-9_]+",1,20)
            require(name not in scores)
            plus,minus,*tasks = map(int,nums)
            within(plus,0,50)
            within(minus,0,50)
            for j,x in enumerate(tasks,1):
                require(x==0 or 150*j<=x<=500*j)
            scores[name] = sum(tasks)+100*plus-50*minus
        best = max(scores.values())
        require(sum(x==best for x in scores.values())==1)
        return max(scores,key=scores.get)+"\n"
    within(n,1,10**5 if pid=="672B" else 2*10**5)
    require(len(w)==n+2 if pid=="699A" else len(w)==2)
    s = token(w[1],r"[a-z]+" if pid=="672B" else r"[LR]+" if pid=="699A" else r"[<>]+",n,n)
    if pid=="672B":
        return str(-1 if n>26 else n-len(set(s)))+"\n"
    if pid=="725A":
        return str(len(s)-len(s.lstrip("<"))+len(s)-len(s.rstrip(">")))+"\n"
    x = array(integers(" ".join(w[2:])),n,0,10**9)
    require(x==sorted(set(x)) and all(v%2==0 for v in x))
    times = [(x[i+1]-x[i])//2 for i in range(n-1) if s[i:i+2]=="RL"]
    return str(min(times) if times else -1)+"\n"


def make_input(pid,rng,mode):
    maximum = mode<0
    if pid=="336A":
        return lines((rng.choice([-1,1])*(10**9 if maximum else rng.randint(1,100)),rng.choice([-1,1])*(10**9 if maximum else rng.randint(1,100))))
    if pid=="727A":
        a = 1 if maximum else rng.randint(1,10**5)
        b = 10**9 if maximum else rng.randint(a+1,10**9)
        if mode%2==0:
            b = a
            for _ in range(rng.randint(1,8)):
                new = b*2 if rng.randrange(2) else b*10+1
                if new>10**9:
                    break
                b = new
        return lines((a,max(a+1,b)))
    if pid=="14B":
        n = 100 if maximum else rng.randint(1,15)
        x = rng.randint(0,1000)
        records = [rng.sample(range(1001),2) for _ in range(n)]
        if mode==-1:
            records = [(0,1000)]*n
        if mode==-2:
            records = [(0,1),(999,1000)]+[(0,1000)]*(n-2)
        return lines((n,x),*records)
    if pid=="43A":
        n = 100 if maximum else rng.choice(range(1,20,2))
        a,b = rng.sample(["ALPHA","BETA","C","DDDDDDDDDD","OTHER"],2)
        goals = [rng.choice((a,b)) for _ in range(n)]
        if goals.count(a)==goals.count(b):
            goals[-1] = b if goals[-1]==a else a
        return lines(n,*goals)
    if pid=="56A":
        n = 100 if maximum else rng.randint(1,20)
        people = [rng.choice(DRINKS+[str(rng.randint(0,1000)),"WATER","TEA","BEERBEER","B"*100,"17","18"]) for _ in range(n)]
        return lines(n,*people)
    if pid=="74A":
        n = 50 if maximum else rng.randint(1,12)
        while True:
            records = [[f"person_{i}",rng.randint(0,50),rng.randint(0,50)]+[rng.choice([0,rng.randint(150*j,500*j)]) for j in range(1,6)] for i in range(n)]
            s = lines(n,*records)
            try:
                output(pid,s)
                return s
            except ValueError:
                pass
    if pid=="106B":
        n = 100 if maximum else rng.randint(1,15)
        prices = rng.sample(range(100,1001),n)
        return lines(n,*[(rng.randint(1000,4200),rng.randint(256,4096),rng.randint(1,500),p) for p in prices])
    if pid=="182B":
        d,n = (10**6,2000) if maximum else (rng.randint(1,100),rng.randint(1,20))
        return lines(d,n,values(n,1,d,mode,rng))
    if pid=="637A":
        n = 1000 if maximum else rng.randint(1,20)
        return lines(n,values(n,1,10**6 if maximum else 5,mode,rng))
    if pid=="670B":
        n = 10**5 if maximum else rng.randint(1,25)
        k = 2*10**9 if maximum else rng.randint(1,n*(n+1)//2)
        ids = list(range(10**9-n+1,10**9+1)) if maximum else rng.sample(range(1,10001),n)
        return lines((n,k),ids)
    if pid in ("672B","699A","725A"):
        n = (10**5 if pid=="672B" else 2*10**5) if maximum else rng.randint(1,35)
        alphabet = "abcdefghijklmnopqrstuvwxyz" if pid=="672B" else "LR" if pid=="699A" else "<>"
        s = alphabet[0]*n if mode==-1 else alphabet[-1]*n if mode==-2 else "".join(rng.choice(alphabet) for _ in range(n))
        if pid=="699A":
            coords = [2*i for i in range(n)] if maximum else sorted(rng.sample(range(0,500000001),n))
            if not maximum:
                coords = [2*i for i in coords]
            return lines(n,s,coords)
        return lines(n,s)
    if pid=="757A":
        n = 10**5 if maximum else rng.randint(1,100)
        s = "B"*n if mode==-1 else ("Bulbasaur"*((n+8)//9))[:n] if mode==-2 else "".join(rng.choice("BulbasaurABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for _ in range(n))
        return lines(s)
    if pid=="844A":
        n = 1000 if maximum else rng.randint(1,35)
        s = "a"*n if mode==-1 else "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
        return lines(s,26 if maximum else rng.randint(1,26))
    raise ValueError("unimplemented replenishment input")


def extras(pid):
    rng = random.Random("1000-replenish-v1-"+pid)
    seen,result = set(),[]
    for mode in [-1,-2,-3]+list(range(180)):
        s = make_input(pid,rng,mode)
        if s in seen:
            continue
        seen.add(s)
        result.append({"input":s,"output":output(pid,s),"caseKind":"max-size" if mode<0 else "boundary-adversarial"})
    return result
