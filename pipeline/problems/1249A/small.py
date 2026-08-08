def case(rnd):
    q = rnd.randint(1, 5)
    lines = [str(q)]
    for _ in range(q):
        hi = rnd.choice([5, 8, 12])
        n = rnd.randint(1, min(6, hi))
        lines.append(str(n))
        lines.append(" ".join(map(str, rnd.sample(range(1, hi + 1), n))))
    return "\n".join(lines) + "\n"
