#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef pair<int,int> ii;
typedef vector<int> vi;
typedef vector< ii > vii;

#define INF 0x3F3F3F3F
#define LINF 0x3F3F3F3F3F3F3F3FLL
#define pb push_back
#define mp make_pair
#define pq priority_queue
#define LSONE(s) ((s)&(-s)) //LASTBIT
#define EPS 1e-7
#define PI  3.1415926535897932384626433832795028841971693993
#define DEG_to_RAD(X)   (X * PI / 180)
#define F first
#define S second

//////////////////////
int dx[] = {1,-1,0,0};
int dy[] = {0,0,-1,1};	
//////////////////////

const int N = 222222; 

int n,m;
ll v1[N],v2[N];
vector< pair<ll,ll> > vet;

int main()
{
	ios::sync_with_stdio(0);
	cin >> n;
	for(int i=0;i<n;++i)
	{
		cin >> v1[i];
		vet.pb(mp(v1[i],0));
	}
	cin >> m;
	for(int i=0;i<m;++i)
	{
		cin >> v2[i];	
		vet.pb(mp(v2[i],1));
	}

	sort(vet.begin(),vet.end());


	ll p1,p2,r1,r2;

	p1 = n*3;
	p2 = m*3;
	r1 = p1;
	r2 = p2;


	for(int i=0;i<n+m;++i)
	{
		if(vet[i].S==0) p1--;
		else p2--;

		if(i+1<n+m && vet[i].F==vet[i+1].F)continue;

		if( (p1-p2 > r1-r2) || (p1-p2 == r1-r2 && p1>r1) )
		{
			r1 = p1;
			r2 = p2;
		}
	}
	cout << r1 << ":" << r2 << endl;
	return 0;
}