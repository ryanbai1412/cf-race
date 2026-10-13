#include <iostream>
#include <cstring>
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;
#define inf 1000000000
#define maxn 2022

int n;
char s[maxn];
int nH, nT;

int Solve(char *s) {
	int res = inf;
	int tmp = 0;
	for (int i = 1; i <= nH; i++)
		tmp += s[i] != 'H';
	for (int i = nH + 1; i <= n; i++)
		tmp += s[i] != 'T';
	res = min(res, tmp / 2);
	tmp = 0;
	for (int i = 1; i <= nT; i++) {
		tmp += s[i] != 'T';
	}
	for (int i = nT + 1; i <= n; i++) {
		tmp += s[i] != 'H';
	}
	res = min(res, tmp / 2);
	return res;
}


int main() {
	nH = nT = 0;
	scanf("%d", &n);
	scanf("%s", s + 1);
	for (int i = 1; i <= n; i++)
		if (s[i] == 'H') nH++; else nT++;
	for (int i = n + 1; i <= n * 2; i++) {
		s[i] = s[i - n];
	} 
	int ans = inf;
	for (int i = 1; i <= n; i++)
		ans = min(ans, Solve(s + i - 1));
	printf("%d\n", ans);
	return 0;
}