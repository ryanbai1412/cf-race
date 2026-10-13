n, s = map(int, input().split())
passengers = []
for i in range(n):
 f, t = map(int, input().split())
 passengers.append({f: t})
time = 0
for f in range(s, 0, -1):
 ts = []
 for passenger in passengers:
     if passenger.get(f) is not None and passenger.get(f) > 0:
         ts.append(passenger[f])
 if len(ts) != 0:
     time += max(ts)
     for passenger in passengers:
         passenger[list(passenger.keys())[0]] -= max(ts)
 time += 1
 for passenger in passengers:
     passenger[list(passenger.keys())[0]] -= 1

print(time)