#include<bits/stdc++.h>
using namespace std;
#define sd(x) scanf("%d",&x)
#define slld(x) scanf("%lld",&x)
#define ss(x) scanf("%s",x)
#define mod 1000000007
#define bitcount __builtin_popcountll
#define ll long long
#define pb push_back
#define pi pair<int,int>
#define pii pair<pi,int>
#define mp make_pair
set<int>s[100005];
int color[100005];
int main()
{
	int i,j,k;
	int n,m;
	sd(n);
	sd(m);
	for(i=1;i<=n;i++)
		sd(color[i]);
	for(i=0;i<m;i++)
	{
		sd(j);
		sd(k);
		if(color[j]!=color[k]){
		s[color[j]].insert(color[k]);
		s[color[k]].insert(color[j]);
	}
	}
	int ans=0;
	int pos=1e6;
	for(i=1;i<=n;i++)
	{
		pos=min(pos,color[i]);
	}
	for(i=1;i<=n;i++)
	{
		int x=s[i].size();
		if(x>ans)
		{
			ans=x;
			pos=i;
		}
	}
	printf("%d\n", pos);
	return 0;
}