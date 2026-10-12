from rlib import *

FACES = {"Tetrahedron": 4, "Cube": 6, "Octahedron": 8, "Dodecahedron": 12, "Icosahedron": 20}
CONSTRAINTS = "n in 1..2*10^5; n lines, each one of the five polyhedron names."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: total faces (4, 6, 8, 12, 20)."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 200000)
    need(len(ls) == n + 1 and all(s in FACES for s in ls[1:]), "n names")


def solve(inp):
    return str(sum(FACES[s] for s in lines(inp)[1:]))


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 2000), rng.randint(1, 3000)])
    return f"{n}\n" + "\n".join(rng.choice(list(FACES)) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single cube", "1\nCube\n"), ("adversarial", "one of each", "5\nTetrahedron\nCube\nOctahedron\nDodecahedron\nIcosahedron\n"),
            ("maxSize", "2*10^5 icosahedrons", "200000\n" + "Icosahedron\n" * 200000)]
