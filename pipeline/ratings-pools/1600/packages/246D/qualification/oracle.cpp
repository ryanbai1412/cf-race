/*cf_246d.cpp @ 2012年11月21日 23时52分03秒 BY dOMhOW*/
#include	<stdlib.h>
#include	<stdio.h>
#include	<string.h>
#include	<math.h>
#include	<map>
#include	<algorithm>
#include	<vector>
#include	<set>
#include	<iostream>
#include	<string>
using namespace std;
#define CC(x,i) do{memset(x,i,sizeof(x));}while(0)
#define inf 0x7f7f7f7f
#define PII pair<int,int>
#define VI vector<int>
#define mp make_pair
#define X first
#define Y second
#define pb push_back
#define lb lower_bound
#define ub upper_bound
#define all(x) x.begin(),x.end()
#define uniq(x) do{sort(all(x));x.resize(unique(all(x))-x.begin());}while(0)
#define two(x) (1ll<<(x))
#define forn(i,l,r) for(int i=(int)(l);i<(int)(r);i++)
#define rep(i,x) for(int i=0;i<(int)(x);i++)

typedef long long  LL;
int c[100009],tj[100009]={0};
set< PII > ss;
int main ( int argc, char *argv[] )
{
	rep(i,100009)tj[i]=-1;
	int n;cin>>n;
	int m;
	cin>>m;
	rep(i,n){cin>>c[i+1];tj[c[i+1]]=0;}
	PII tmp;
	rep(i,m){
		int a,b;
		cin>>a>>b;
		tmp.X=c[a];tmp.Y=c[b];
		if(tmp.X==tmp.Y)continue;
		if(tmp.X>tmp.Y)swap(tmp.X,tmp.Y);
		if(ss.find(tmp)==ss.end()){
			ss.insert(tmp);
			tj[tmp.X]++;tj[tmp.Y]++;
		//	cout<<"add "<<tmp.X<<","<<tmp.Y<<endl;
		}
	}
	int mx=-1,who;
	rep(i,100009){
		if(tj[i]>mx){mx=tj[i],who=i;}
	}
	cout<<who<<endl;
	return EXIT_SUCCESS;
}