def case(rnd):
    t = rnd.randint(1, 8)
    lines = [str(t)]
    for _ in range(t):
        n = rnd.randint(2, 8)
        a = rnd.randint(1, n)
        b = rnd.randint(1, n)
        while b == a:
            b = rnd.randint(1, n)
        lines.append(f"{n} {rnd.randint(0, 10)} {a} {b}")
    return "\n".join(lines) + "\n"
