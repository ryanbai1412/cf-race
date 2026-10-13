#define _CRT_SECURE_NO_WARNINGS

#include<bits/stdc++.h>

#define all(v)              ((v).begin()), ((v).end())

#define allr(v)             ((v).rbegin()), ((v).rend())

#define sz(v)               ((int)((v).size()))

#define clr(v, d)           memset(v, d, sizeof(v))

#define MP                  make_pair

#define lpv(i, v)           for(int i=0;i<sz(v);++i)

#define lpn(i, n)           for(int i=0;i<(int)(n);++i)

#define PI                  3.14159265359

#define pb                  push_back

#define ull                 unsigned long long

#define ll                  long long

#define LD                  long double

#define vi                  vector<int>

#define vl                  vector<ll>

#define vs                  vector<string>

using namespace std;

const ll MOD = 1e6 + 3;

int main()

{

	int d, n, ans = 0;

	scanf("%d%d", &d, &n);

	for (int i = 0;i < n;i++)

	{

		int a;

		scanf("%d", &a);

		if (i + 1 < n)

			ans += abs(d - a);

	}

	printf("%d\n", ans);

	return 0;

}