#include <iostream>
#include <set>
#include <map>
#include <queue>
#include <stack>
#include <algorithm>
#include <vector>
#include <string>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <sstream>
using namespace std;

typedef long long ll;
typedef vector<int> vi;
typedef vector<string> vs;
typedef pair<int,int> pii;
#define sz(A) (int)(A).size()
#define FOR(A,B) for(int A=0; A < (int) (B);A++)
#define pb push_back
#define all(x) x.begin() , x.end()

#define N 50001
vi adj[N];
int pai[N];

void dfs(int v, int p) {
	pai[v] = p;
	for(int i = 0; i < sz(adj[v]); i++) {
		if(adj[v][i] != p) {
			dfs(adj[v][i], v);
		}
	}
}

int main() {
	int n,r1,r2;
	scanf("%d %d %d", &n, &r1, &r2);
	for(int i = 1; i <= n; i++) {
		adj[i].clear();
	}
	for(int i = 1; i <= n; i++) {
		if(i == r1) continue;
		int pp;
		scanf("%d", &pp);
		adj[i].push_back(pp);
		adj[pp].push_back(i);
	}

	dfs(r2, -1);
	int prim = 1;
	for(int i = 1; i <= n; i++) {
		if(pai[i] != -1) {
			if(prim) {
				printf("%d", pai[i]);
				prim = 0;
			} else {
				printf(" %d", pai[i]);
			}
		}
	}
	printf("\n");

    return 0;
}