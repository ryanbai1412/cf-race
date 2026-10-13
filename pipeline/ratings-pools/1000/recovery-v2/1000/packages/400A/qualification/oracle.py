t = int(input())
N = 12
divisors = [1,2,3,4,6,12]
L = 6

for _ in range(t):
    cards = input()
    goodDivs = []
    for k in range(L):
        numCols = divisors[k]
        state = [True] * numCols
        for m in range(N):
            if cards[m] == 'O':
                state[m % numCols] = False
        if any(state):
            goodDivs.append(numCols)

    print(len(goodDivs), end=' ')
    for k in range(len(goodDivs)-1, -1, -1):
        print(f"{N//goodDivs[k]}x{goodDivs[k]}", end=' ')
    print()