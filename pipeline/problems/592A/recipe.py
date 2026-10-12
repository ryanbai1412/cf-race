from genlib import *  # noqa: F401,F403

CHECKER = "Winner A/B; statement guarantees a winner; exact token comparison."
STATEMENT = "Legend (A moves white up first, B black down, optimal play), input 8x8 board, output present."


def solve(s):
    b = s.split()
    wa, wb = 99, 99
    for c in range(8):
        col = [b[r][c] for r in range(8)]
        for r in range(8):
            if col[r] == "W" and all(col[i] == "." for i in range(r)):
                wa = min(wa, r)
            if col[r] == "B" and all(col[i] == "." for i in range(r + 1, 8)):
                wb = min(wb, 7 - r)
    return ("A" if wa <= wb else "B") + "\n"


def board(g, dw, db):
    rows = [["."] * 8 for _ in range(8)]
    for r in range(8):
        for c in range(8):
            x = g.random()
            if x < dw and r > 0:
                rows[r][c] = "W"
            elif x < dw + db and r < 7:
                rows[r][c] = "B"
    return fmt(*["".join(r) for r in rows])


def free(b, side):
    if side == "W":
        return any(b[r][c] == "W" and all(b[i][c] == "." for i in range(r)) for r in range(8) for c in range(8))
    return any(b[r][c] == "B" and all(b[i][c] == "." for i in range(r + 1, 8)) for r in range(8) for c in range(8))


def gen(g, dw, db):
    while True:
        t = board(g, dw, db)
        b = t.split()
        if free(b, "W") and free(b, "B"):
            return t


def cases(g):
    e = "........"
    out = [("boundary", "white on row 2, one move", fmt(e, "W.......", e, e, e, e, "......B.", e)),
           ("boundary", "black on row 7, one move", fmt(e, e, e, e, e, "W.......", ".......B", e)),
           ("adversarial", "equal distances: A moves first and wins", fmt(e, e, e, "W.......", ".......B", e, e, e)),
           ("adversarial", "closer white pawn blocked by black in its column", fmt(e, "B.......", "W.......", e, e, e, "..B.....", ".W......")),
           ("adversarial", "black one step closer than white", fmt(e, e, e, e, "W.......", ".....B..", e, e)),
           ("maxSize", "dense board", gen(g, 0.3, 0.3)), ("maxSize", "very dense random board", gen(g, 0.4, 0.4))]
    out += fill(g, lambda g: gen(g, g.random() * 0.2, g.random() * 0.2), 120)
    return out
