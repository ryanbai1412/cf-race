def case(rnd):
    t = rnd.randint(1, 4)
    lines = [str(t)]
    for _ in range(t):
        n = rnd.randint(2, 7)
        k1 = rnd.randint(1, n - 1)
        a = rnd.sample(range(1, n + 1), k1)
        b = [v for v in range(1, n + 1) if v not in set(a)]
        rnd.shuffle(b)
        lines.append(f"{n} {len(a)} {len(b)}")
        lines.append(" ".join(map(str, a)))
        lines.append(" ".join(map(str, b)))
    return "\n".join(lines) + "\n"
