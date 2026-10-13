#include <bits/stdc++.h>
using namespace std;
#define mp make_pair
#define boost ios_base::sync_with_stdio(false)
#define pb push_back
#define e1 first
#define e2 second
#define tysiac 1010
#define milion 1000100
#define OUT(x) { cout << x; return 0; }
#define scanf(...) scanf(__VA_ARGS__)?:0
typedef long long int ll;
typedef unsigned int ui;
typedef unsigned long long ull;
typedef double ld;
typedef pair <int, int> PII;
typedef pair <PII, int> PPI;
typedef pair <ll, ll> PLL;
typedef pair <ld, ld> PDD;
typedef pair <PII, PII> PP;
typedef pair <ll, int> PLI;
const int mod = 1e9+7;
const int inf = 1e9+9;
const int MOD = 1e9+696969;
const ll INF = 1e18+3;

int n, m, a, b, c,d, k, h;
#define maxn 1000100
vector <int> v[maxn];
bool odw[maxn];
int wyn = 0, parent[maxn], CYCLE;

void dfs(int x)
{
	odw[x] = 1;
	for (auto u : v[x])
	if (!odw[u])
	{
		parent[u] = x;
		dfs(u);
	}
	else if (odw[u] && u != parent[x]) h = 1;
}
int main()
{
boost;
	cin >> n >> m;
	for (int i=1; i<=m; ++i)
	{
		cin >> a >> b;
		v[a].pb(b);
		v[b].pb(a);
	}
	for (int i=1; i<=n; ++i)
	if (!odw[i])
	{
		h = 0;
		dfs(i);
		if (!h) ++wyn;
	}
	cout << wyn;
}