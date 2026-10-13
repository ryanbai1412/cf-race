#include <bits/stdc++.h>

using namespace std;



#define loop(i,n) for(int i = 0;i < int(n);i++)

#define rloop(i,n) for(int i = int(n);i >= 0;i--)

#define range(i,a,b) for(int i = int(a);i <= int(b);i++)

#define INF	1e9

#define SZ(c) int(c.size())

#define ALL(c) c.begin(), c.end()

#define RALL(c) c.rbegin(), c.rend()

#define PI acos(-1)

#define pb push_back

#define mp make_pair

#define fr first

#define sc second



typedef vector<int> vi;

typedef vector<pair<int,int> > vii;

typedef long long ll;

typedef pair<int, int> pii;



int n,m;

const int N=6+1e5;

vi Adj[N];

bool vis[N];

int color[N];

int cnt[N];

map <pii,bool> ma;



void dfs(int u){

    vis[u]=1;

    loop(i,SZ(Adj[u])){

        int v=Adj[u][i];

        if(color[v] != color[u] && !ma[mp(color[u],color[v])]){

            cnt[color[u]]++;

            cnt[color[v]]++;

            ma[mp(color[u],color[v])]=1;

            ma[mp(color[v],color[u])]=1;

        }

        if(!vis[v])dfs(v);

    }

}





int main()

{



#ifndef ONLINE_JUDGE

	//freopen("in.in", "r", stdin);

	//freopen("out.in", "w", stdout);

#endif



    int a,b,mx=0,mn=N;

    scanf("%d %d",&n ,&m);

    range(i,1,n)scanf("%d",&color[i]);

    loop(i,m){

        scanf("%d %d",&a ,&b);

        Adj[a].pb(b);

        Adj[b].pb(a);

    }



    range(i,1,n)if(!vis[i])dfs(i);

    range(i,1,n)mx=max(mx,cnt[color[i]]);

    range(i,1,n){

        if(cnt[color[i]] == mx){

            mn=min(mn,color[i]);

        }

    }



    printf("%d\n",mn);



    return 0;

}