from collections import Counter

while True:
    m, n = (int(s) for s in input().split())
    if not m:
        break

    objects = [int(input(), 2) for i in range(n)]
    dp = [bytearray(1 << m) for i in range(1 << m)]
    bits = [1 << i for i in range(m)]

    for asked in reversed(range((1 << m) - 1)):
        for masked, count in Counter(obj & asked for obj in objects).items():
            if count > 1:
                dp[asked][masked] = min(max(dp[asked + b][masked],
                                            dp[asked + b][masked + b])
                                        for b in bits if not b & asked) + 1
    print(dp[0][0])