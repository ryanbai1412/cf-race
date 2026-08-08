def case(rnd):
    t = rnd.randint(1, 10)
    lines = [str(t)]
    for _ in range(t):
        hi = rnd.choice([5, 20, 60])
        lines.append(f"{rnd.randint(0, hi)} {rnd.randint(0, hi)}")
    return "\n".join(lines) + "\n"
