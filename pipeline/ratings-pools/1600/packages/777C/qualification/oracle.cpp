#include<bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef pair<int, int> PII;

const int MM = 1e9 + 7;
const double eps = 1e-8;
const int MAXN = 2e6 + 10;

int n, m;

void prework(){

}

void read(){

}

vector<int> a[MAXN];
struct Pt{
	int l, r, t;
} f[MAXN];

int ans[MAXN];

void solve(int casi){
	scanf("%d%d", &n, &m);
	for(int i = 1; i <= n; i++){
		a[i].resize(m + 1);
		for(int j = 1; j <= m; j++)
			scanf("%d", &a[i][j]);
	}
	int Q, QQ;
	scanf("%d", &Q);
	for(int i = 1; i <= Q; i++){
		scanf("%d%d", &f[i].l, &f[i].r);
		f[i].t = -i;
	}
	QQ = Q;
	for(int j = 1; j <= m; j++){
		int pre = 1;
		for(int i = 2; i <= n; i++){
			if (a[i][j] < a[i-1][j]){
				Q++;
				f[Q].l = pre, f[Q].r = i - 1;
				f[Q].t = 0;
				pre = i;
			}
		}
		Q++;
		f[Q].l = pre, f[Q].r = n;
		f[Q].t = 0;
	}
//	for(int i = 1; i <= Q; i++)
//		cout<<f[i].l<<' '<<f[i].r<<' '<<f[i].t<<endl;
	sort(f + 1, f + Q + 1, [](const Pt & a, const Pt & b){
		if (a.l == b.l){
			return a.t > b.t;
		}
		else return a.l < b.l;
	});
	int rm = -1;
	for(int i = 1; i <= Q; i++){
		if (f[i].t == 0){
			rm = max(rm, f[i].r);
		}
		else{
			ans[-f[i].t] = (rm >= f[i].r);
		}
	}
	for(int i = 1; i <= QQ; i++)
		puts(ans[i] ? "Yes" : "No");
}

void printans(){

}


int main(){
	prework();
	int T = 1;
//	cin>>T;
	for(int i = 1; i <= T; i++){
		read();
		solve(i);
		printans();
	}
	return 0;
}