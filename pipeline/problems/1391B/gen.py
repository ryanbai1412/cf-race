import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(grid):
    n, m = len(grid), len(grid[0])
    g = [row[:] for row in grid]
    g[n - 1][m - 1] = "C"
    return f"{n} {m}\n" + "\n".join("".join(r) for r in g)


def rand_grid(rnd, n, m, p=0.5):
    return [[("R" if rnd.random() < p else "D") for _ in range(m)] for _ in range(n)]


def main(outdir):
    rnd = random.Random(1391)
    w = Writer(outdir)

    # 1x1 grid (already functional) and other minimal shapes
    w.add(multi([case([["C"]]), case([["R", "R"]]), case([["D"], ["D"]]),
                 case([["R", "D"], ["D", "R"]])]))
    # max size, all R / all D / worst case (last row all D, last col all R)
    N = M = 100
    w.add(multi([case([["R"] * M for _ in range(N)]),
                 case([["D"] * M for _ in range(N)])]))
    worst = rand_grid(rnd, N, M)
    for j in range(M):
        worst[N - 1][j] = "D"
    for i in range(N):
        worst[i][M - 1] = "R"
    w.add(multi([case(worst)]))
    # already functional max grid: last row R, last col D
    good = rand_grid(rnd, N, M)
    for j in range(M):
        good[N - 1][j] = "R"
    for i in range(N):
        good[i][M - 1] = "D"
    w.add(multi([case(good)]))
    # single row / single column at max length
    w.add(multi([case([rand_grid(rnd, 1, 100)[0]]),
                 case(rand_grid(rnd, 100, 1))]))
    # 10 random max-size tests (t = 10)
    for _ in range(6):
        w.add(multi([case(rand_grid(rnd, 100, 100)) for _ in range(10)]))
    # random small grids
    for _ in range(6):
        cases = []
        for _ in range(10):
            n = rnd.randint(1, 8)
            m = rnd.randint(1, 8)
            cases.append(case(rand_grid(rnd, n, m, rnd.choice([0.2, 0.5, 0.8]))))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
