import sys
from sys import stdin
input = stdin.readline

n = int(input())
a = list(map(int, input().split()))
t, k = [], 0
for i in range(n):
	if k > 0:
		if a[i] == a[i-1]:
			t.append(k)
			k = 0
	k += 1
if k > 0: t.append(k)
ans = k = 0
for i in range(len(t)):
	k += t[i]
	if i > 2: k -= t[i-3]
	ans = max(ans, k)
print(ans)
