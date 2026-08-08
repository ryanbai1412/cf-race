def case(rnd):
    q = rnd.randint(1, 8)
    lines = [str(q)]
    for _ in range(q):
        n = rnd.randint(1, 6)
        lines.append(str(n))
        lines.append(" ".join(str(rnd.randint(1, 15)) for _ in range(n)))
    return "\n".join(lines) + "\n"
