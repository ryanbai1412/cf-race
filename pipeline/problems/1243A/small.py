def case(rnd):
    k = rnd.randint(1, 5)
    lines = [str(k)]
    for _ in range(k):
        n = rnd.randint(1, 9)
        lines.append(str(n))
        lines.append(" ".join(str(rnd.randint(1, n)) for _ in range(n)))
    return "\n".join(lines) + "\n"
