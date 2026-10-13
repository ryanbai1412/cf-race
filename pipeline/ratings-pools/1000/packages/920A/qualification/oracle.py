for _ in range(int(input())):
    n, k = map(int, input().split())
    taps = list(map(int, input().split()))
    ans = max(taps[0]-1, n-taps[-1])
    for i in range(k-1):
        ans = max(ans, (taps[i+1]-taps[i])//2)
    print(ans+1)