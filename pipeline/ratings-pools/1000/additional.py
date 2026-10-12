"""Reviewed unique-answer integer/token tasks; deterministic full-domain generators."""
from collections import Counter
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import random
import re

from recipes import integers, within
from input_layout import layout

IDS = tuple("1A 13A 90A 106A 109A 118A 118B 122A 122B 195A 259A 268B 272A 368A 371A 379A 385A 389A 435A 535A 579A 604A 610A 620B 628A 660B 724A 733A 761A 779A 798A 804A 816A 831A 847M 849A 862A 864B 886A 887A 888B 893B 909A 990A 991A".split())
REVIEW = json.loads(Path(__file__).with_name("statement-review.json").read_text())
RULES = {pid: REVIEW[pid]["input_format"] + " Unique output; deterministic authored oracle below implements the retained problem description." for pid in IDS}
NUMERIC = {
    "1A": ((1,10**9),)*3, "13A": ((3,1000),), "90A": ((0,100),)*3,
    "109A": ((1,10**6),), "118B": ((2,9),), "122A": ((1,1000),),
    "195A": ((2,1000),(1,999),(1,1000)), "268B": ((1,2000),),
    "379A": ((1,1000),(2,1000)), "535A": ((0,99),), "579A": ((1,10**9),),
    "610A": ((1,2*10**9),), "620B": ((1,10**6),)*2, "628A": ((1,500),)*3,
    "660B": ((1,100),(1,400)), "761A": ((0,100),)*2, "804A": ((1,10**5),),
    "886A": ((0,1000),)*6, "893B": ((1,10**5),),
    "990A": ((1,10**12),(1,10**12),(1,100),(1,100)), "991A": ((0,100),)*4,
}


def token(word, pattern, low, high):
    if not low <= len(word) <= high or not re.fullmatch(pattern, word):
        raise ValueError("invalid string domain")
    return word


def require(condition):
    if not condition:
        raise ValueError("invalid dependent constraint")


def array(values, n, low, high):
    require(len(values) == n)
    for v in values:
        within(v,low,high)
    return values


def yn(condition):
    return "YES\n" if condition else "NO\n"


def numeric(pid, v):
    require(len(v) == len(NUMERIC[pid]))
    for x,(lo,hi) in zip(v,NUMERIC[pid]):
        within(x,lo,hi)
    if pid == "1A":
        n,m,a = v
        return (n+a-1)//a*((m+a-1)//a)
    if pid == "13A":
        a, = v
        total = 0
        for base in range(2,a):
            x = a
            while x:
                total += x % base
                x //= base
        divisor = math.gcd(total,a-2)
        return f"{total//divisor}/{(a-2)//divisor}"
    if pid == "90A":
        require(sum(v)>0)
        return max(30+i+3*((count-1)//2) for i,count in enumerate(v) if count)
    if pid == "109A":
        n, = v
        for sevens in range(n//7,-1,-1):
            rest = n-7*sevens
            if rest % 4 == 0:
                return "4"*(rest//4)+"7"*sevens
        return -1
    if pid == "118B":
        n, = v
        lines = []
        for h in list(range(n+1))+list(range(n-1,-1,-1)):
            values = list(range(h+1))+list(range(h-1,-1,-1))
            lines.append(" "*(2*(n-h))+" ".join(map(str,values)))
        return "\n".join(lines)
    if pid == "122A":
        n, = v
        lucky = [int("".join(s)) for length in range(1,4) for s in itertools.product("47",repeat=length)]
        return "YES" if any(n%x==0 for x in lucky) else "NO"
    if pid == "195A":
        a,b,c = v
        require(a>b)
        return (c*(a-b)+b-1)//b
    if pid == "268B":
        n, = v
        return n+sum((n-known)*known for known in range(1,n))
    if pid == "379A":
        a,b = v
        answer,stubs = a,a
        while stubs>=b:
            new,rem = divmod(stubs,b)
            answer += new
            stubs = new+rem
        return answer
    if pid == "535A":
        n, = v
        first = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
        tens = "twenty thirty forty fifty sixty seventy eighty ninety".split()
        return first[n] if n<20 else tens[n//10-2]+("-"+first[n%10] if n%10 else "")
    if pid == "579A":
        return v[0].bit_count()
    if pid == "610A":
        n, = v
        return 0 if n%2 else max(0,(n//2-1)//2)
    if pid == "620B":
        a,b = v
        require(a<=b)
        prefix = segment_prefix()
        return prefix[b]-prefix[a-1]
    if pid == "628A":
        n,b,p = v
        return f"{(n-1)*(2*b+1)} {n*p}"
    if pid == "660B":
        n,m = v
        require(m<=4*n)
        return " ".join(str(x) for i in range(1,2*n+1) for x in (i+2*n,i) if x<=m)
    if pid == "761A":
        a,b = v
        return "YES" if a+b>0 and abs(a-b)<=1 else "NO"
    if pid == "804A":
        return (v[0]-1)//2
    if pid == "886A":
        return "YES" if any(2*sum(c)==sum(v) for c in itertools.combinations(v,3)) else "NO"
    if pid == "893B":
        n, = v
        return max((2**k-1)*2**(k-1) for k in range(1,10) if n%((2**k-1)*2**(k-1))==0)
    if pid == "990A":
        n,m,a,b = v
        rem = n%m
        return min(rem*b,(m-rem)*a) if rem else 0
    if pid == "991A":
        a,b,c,n = v
        absent = n-(a+b-c)
        return absent if c<=min(a,b) and absent>=1 else -1
    raise ValueError("unimplemented numeric problem")


@lru_cache(maxsize=1)
def segment_prefix():
    from array import array as int_array
    counts = (6,2,5,5,4,5,6,3,7,6)
    prefix = int_array("I",[0])
    for i in range(1,10**6+1):
        prefix.append(prefix[-1]+sum(counts[int(x)] for x in str(i)))
    return prefix


def output(pid,text):
    if pid in NUMERIC:
        return str(numeric(pid,integers(text)))+"\n"
    words = text.split()
    if pid == "106A":
        require(len(words)==3 and words[0] in "SHDC" and len(words[0])==1)
        trump,a,b = words
        token(a,r"[6789TJQKA][SHDC]",2,2)
        token(b,r"[6789TJQKA][SHDC]",2,2)
        require(a!=b)
        return yn((a[1]==b[1] and "6789TJQKA".index(a[0])>"6789TJQKA".index(b[0])) or (a[1]!=b[1] and a[1]==trump))
    if pid in ("118A","122B","733A","798A","887A"):
        require(len(words)==1)
        s = words[0]
        spec = {"118A":(r"[A-Za-z]+",100),"122B":(r"[0-9]+",50),"733A":(r"[A-Z]+",100),"798A":(r"[a-z]+",15),"887A":(r"[01]+",100)}
        pattern,limit = spec[pid]
        token(s,pattern,1,limit)
        if pid == "118A":
            s = s.lower()
            require(any(x not in "aoyeui" for x in s))
            return "".join("."+x for x in s if x not in "aoyeui")+"\n"
        if pid == "122B":
            a,b = s.count("4"),s.count("7")
            return ("-1" if not a+b else "4" if a>=b else "7")+"\n"
        if pid == "733A":
            points = [0]+[i+1 for i,c in enumerate(s) if c in "AEIOUY"]+[len(s)+1]
            return str(max(b-a for a,b in zip(points,points[1:])))+"\n"
        if pid == "798A":
            mismatches = sum(s[i]!=s[-i-1] for i in range(len(s)//2))
            return yn(mismatches==1 or (mismatches==0 and len(s)%2==1))
        if pid == "887A":
            return yn("1" in s and s[s.index("1")+1:].count("0")>=6)
    if pid == "259A":
        require(len(words)==8)
        for row in words:
            token(row,r"[WB]+",8,8)
        return yn(all(all(a!=b for a,b in zip(row,row[1:])) for row in words))
    if pid == "724A":
        days = "monday tuesday wednesday thursday friday saturday sunday".split()
        require(len(words)==2 and all(s in days for s in words))
        return yn((days.index(words[1])-days.index(words[0]))%7 in (0,2,3))
    if pid == "816A":
        require(len(words)==1)
        token(words[0],r"[0-9]{2}:[0-9]{2}",5,5)
        h,m = map(int,words[0].split(":"))
        within(h,0,23)
        within(m,0,59)
        for wait in range(1440):
            now = (h*60+m+wait)%1440
            s = f"{now//60:02}:{now%60:02}"
            if s==s[::-1]:
                return str(wait)+"\n"
    if pid == "909A":
        require(len(words)==2)
        a,b = words
        token(a,r"[a-z]+",1,10)
        token(b,r"[a-z]+",1,10)
        return min(a[:i]+b[:j] for i in range(1,len(a)+1) for j in range(1,len(b)+1))+"\n"
    if pid in ("864B","888B"):
        require(len(words)==2 and words[0].isdigit())
        n = int(words[0])
        within(n,1,200 if pid=="864B" else 100)
        s = token(words[1],r"[A-Za-z]+" if pid=="864B" else r"[UDLR]+",n,n)
        if pid == "864B":
            return str(max(map(lambda w:len(set(w)),re.split("[A-Z]",s))))+"\n"
        return str(2*(min(s.count("U"),s.count("D"))+min(s.count("L"),s.count("R"))))+"\n"
    v = integers(text)
    if pid == "604A":
        require(len(v)==12)
        array(v[:5],5,0,119)
        array(v[5:10],5,0,10)
        array(v[10:],2,0,20)
        score = sum(max(150*i,500*i-2*i*m-50*w) for i,(m,w) in enumerate(zip(v[:5],v[5:10]),1))
        return str(score+100*v[10]-50*v[11])+"\n"
    if pid in ("272A","368A","371A","385A","435A"):
        require(len(v)>=2)
        n,parameter = v[:2]
        within(n,2 if pid=="385A" else 1,100)
        if pid == "272A":
            needs = array(v[1:],n,1,5)
            return str(sum((sum(needs)+x)%(n+1)!=1 for x in range(1,6)))+"\n"
        if pid == "368A":
            within(parameter,1,100)
            require(len(v)==n+3)
            prices = array(v[2:-1],n,1,100)
            m = v[-1]
            within(m,1,100)
            return str(sum(sorted(prices)[:m])-max(0,m-n)*parameter)+"\n"
        if pid == "371A":
            within(parameter,1,n)
            require(n%parameter==0)
            a = array(v[2:],n,1,2)
            return str(sum(min(a[i::parameter].count(1),a[i::parameter].count(2)) for i in range(parameter)))+"\n"
        if pid == "385A":
            within(parameter,0,100)
            a = array(v[2:],n,0,100)
            return str(max([0]+[a[i]-a[i+1]-parameter for i in range(n-1)]))+"\n"
        within(parameter,1,100)
        a = array(v[2:],n,1,parameter)
        buses,load = 1,0
        for x in a:
            if load+x>parameter:
                buses,load = buses+1,0
            load += x
        return str(buses)+"\n"
    if pid in ("389A","779A","831A","847M","849A","862A"):
        n = v[0]
        within(n,2 if pid in ("389A","847M") else 1,100)
        if pid == "862A":
            require(len(v)==n+2)
            x = v[1]
            within(x,0,100)
            a = array(v[2:],n,0,100)
            require(len(set(a))==n)
            return str(sum(i not in a for i in range(x))+(x in a))+"\n"
        if pid == "779A":
            require(len(v)==2*n+1)
            a = array(v[1:n+1],n,1,5)
            b = array(v[n+1:],n,1,5)
            ca,cb = Counter(a),Counter(b)
            if any((ca[i]+cb[i])%2 for i in range(1,6)):
                return "-1\n"
            return str(sum(abs(ca[i]-cb[i]) for i in range(1,6))//4)+"\n"
        a = array(v[1:],n,-1000 if pid=="847M" else 0 if pid=="849A" else 1,1000 if pid in ("847M","831A") else 100)
        if pid == "389A":
            return str(n*math.gcd(*a))+"\n"
        if pid == "847M":
            d = a[1]-a[0]
            return str(a[-1]+(d if all(y-x==d for x,y in zip(a,a[1:])) else 0))+"\n"
        if pid == "849A":
            return yn(n%2==1 and a[0]%2==1 and a[-1]%2==1)
        phase = 0
        for x,y in zip(a,a[1:]):
            if y>x:
                if phase:
                    return "NO\n"
            elif y==x:
                if phase==2:
                    return "NO\n"
                phase = 1
            else:
                phase = 2
        return "YES\n"
    raise ValueError("unimplemented reviewed problem")


def flat(*values):
    return " ".join(map(str,values))+"\n"


def inputs(pid):
    rng = random.Random("1000-reviewed-v1-"+pid)
    small,maximum = [],[]
    if pid in NUMERIC:
        bounds = NUMERIC[pid]
        candidates = list(itertools.product(*[(lo,hi) for lo,hi in bounds]))
        candidates += [tuple(rng.randint(lo,hi) for lo,hi in bounds) for _ in range(60)]
        if len(bounds)==1:
            candidates += [(i,) for i in range(bounds[0][0],min(bounds[0][1]+1,32))]
        for v in candidates:
            if pid=="90A" and not sum(v):
                continue
            if pid=="195A" and v[0]<=v[1]:
                continue
            if pid=="620B" and v[0]>v[1]:
                v = tuple(sorted(v))
            if pid=="660B" and v[1]>4*v[0]:
                continue
            small.append(flat(*v))
        maximum = [s for s in small if any(int(x)==hi for x,(_,hi) in zip(s.split(),bounds))]
        return small,maximum
    if pid=="106A":
        cards = [a+b for a in "6789TJQKA" for b in "SHDC"]
        small = [flat(trump,a,b) for trump in "SHDC" for a,b in [rng.sample(cards,2) for _ in range(40)]]
        maximum = [flat("S","AS","6H"),flat("S","6S","AS")]
    elif pid in ("118A","122B","733A","798A","887A"):
        alphabet,limit = {"118A":("aAoeUiYbBcCdDzZ",100),"122B":("0123456789",50),"733A":("ABCDEFYIOU",100),"798A":("abc",15),"887A":("01",100)}[pid]
        small = [rng.choice(alphabet)+"\n" for _ in range(10)]
        small += ["".join(rng.choice(alphabet) for _ in range(rng.randint(1,limit)))+"\n" for _ in range(60)]
        maximum = [c*limit+"\n" for c in alphabet]
        if pid=="118A":
            small = [s for s in small if any(x not in "aoyeui" for x in s.strip().lower())]
            maximum = [s for s in maximum if any(x not in "aoyeui" for x in s.strip().lower())]
        if pid=="887A":
            small += ["0\n","1\n","1000000\n","01000000\n","100000\n","1010101010101\n"]
        if pid=="798A":
            small += ["a\n","aa\n","ab\n","abc\n","aba\n","abca\n","abcde\n"]
    elif pid=="259A":
        small = ["\n".join(rng.choice(["WB"*4,"BW"*4]) for _ in range(8))+"\n" for _ in range(60)]
        small += ["\n".join("".join(rng.choice("WB") for _ in range(8)) for _ in range(8))+"\n" for _ in range(20)]
        maximum = ["\n".join(["W"*8]*8)+"\n","\n".join(["WB"*4]*8)+"\n"]
    elif pid=="724A":
        days = "monday tuesday wednesday thursday friday saturday sunday".split()
        small = [flat(a,b) for a in days for b in days]
        maximum = [flat("sunday","sunday")]
    elif pid=="816A":
        small = [f"{h:02}:{m:02}\n" for h in range(24) for m in (0,1,9,10,11,22,32,33,44,55,58,59)]
        maximum = ["23:59\n","23:32\n"]
    elif pid=="909A":
        small = [flat(a,b) for a in ("a","ab","aba","bac","zz") for b in ("a","b","ba","z")]
        small += [flat(*( "".join(rng.choice("abcxyz") for _ in range(rng.randint(1,10))) for _ in range(2))) for _ in range(60)]
        maximum = [flat("z"*10,"a"*10),flat("a"*10,"z"*10)]
    elif pid in ("864B","888B"):
        alphabet,limit = ("abczABCZ",200) if pid=="864B" else ("UDLR",100)
        small = [flat(n,"".join(rng.choice(alphabet) for _ in range(n))) for n in range(1,61)]
        maximum = [flat(limit,c*limit) for c in alphabet]
        maximum += [flat(limit,(alphabet*((limit+len(alphabet)-1)//len(alphabet)))[:limit])]
    elif pid=="604A":
        small = [flat(*(rng.randint(0,119) for _ in range(5)),*(rng.randint(0,10) for _ in range(5)),rng.randint(0,20),rng.randint(0,20)) for _ in range(60)]
        maximum = [flat(*([119]*5+[10]*5+[20,20])),flat(*([0]*10+[20,0])),flat(*([119]*5+[10]*5+[0,20]))]
    else:
        for rep in range(60):
            n = rng.randint(2 if pid in ("385A","389A","847M") else 1,100)
            small.append(array_input(pid,n,rep,rng))
        maximum = [array_input(pid,100,mode,rng) for mode in (-1,-2,-3)]
    require(bool(small) and bool(maximum))
    return small+maximum,maximum


def array_input(pid,n,mode,rng):
    def values(low,high):
        return ([low]*n if mode==-1 else [high]*n if mode==-2 else [low if i%2 else high for i in range(n)] if mode==-3 else [rng.randint(low,high) for _ in range(n)])
    if pid=="272A":
        return flat(n,*values(1,5))
    if pid=="368A":
        return flat(n,100 if mode<0 else rng.randint(1,100),*values(1,100),100 if mode<0 else rng.randint(1,100))
    if pid=="371A":
        k = 1 if mode==-1 else n if mode==-2 else rng.choice([i for i in range(1,n+1) if n%i==0])
        return flat(n,k,*values(1,2))
    if pid=="385A":
        return flat(n,100 if mode==-1 else 0 if mode<0 else rng.randint(0,100),*values(0,100))
    if pid=="435A":
        m = 100 if mode<0 else rng.randint(1,100)
        return flat(n,m,*values(1,m))
    if pid=="389A":
        return flat(n,*values(1,100))
    if pid=="779A":
        a = values(1,5)
        b = a[:] if mode==-1 else list(reversed(a)) if mode==-2 else values(1,5)
        return flat(n,*a,*b)
    if pid=="831A":
        return flat(n,*values(1,1000))
    if pid=="847M":
        return flat(n,*values(-1000,1000))
    if pid=="849A":
        return flat(n,*values(0,100))
    if pid=="862A":
        a = rng.sample(range(101),n)
        return flat(n,100 if mode<0 else rng.randint(0,100),*a)
    raise ValueError("unimplemented array generator")


def extras(pid):
    cases,maximum = inputs(pid)
    seen = set()
    result = []
    for s in cases:
        if s not in seen:
            result.append({"input":layout(pid,s),"output":output(pid,s),"caseKind":"max-size" if s in maximum else "boundary-adversarial"})
            seen.add(s)
    return result
