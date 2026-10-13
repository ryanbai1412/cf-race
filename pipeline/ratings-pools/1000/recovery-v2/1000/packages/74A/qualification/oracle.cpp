#include <bits/stdc++.h>

using namespace std;

typedef long long int ll;
typedef long double ld;

typedef pair<ll, ll> ii;
typedef vector<ll> vi;
typedef vector<pair<ll, ll> > vii;

#define PB push_back

#define FOR(prom,a,b) for ( ll prom = (a); prom < (b); ++prom )
#define F(a) FOR(i,0,a)
#define FF(a) FOR(j,0,a)

#define MM(co, cim) memset( (co), (cim), sizeof((co)) )
#define DEB(x) cerr << ">>> " << #x << " : " << x << endl;

#define EPS (1e-10)
#define INF (1<<29)

int main (){
	ll N;
	cin>>N;
	string best;
	string s;
	ll a, b, c, d, e, p, m;
	ll maxPts=-INF;

	F(N){
		cin>>s>>p>>m>>a>>b>>c>>d>>e;
		ll sum=p*100-m*50+a+b+c+d+e;
		if(sum>maxPts){
			maxPts=sum;
			best=s;
		}
	}
	cout<<best<<endl;

	return 0;
}