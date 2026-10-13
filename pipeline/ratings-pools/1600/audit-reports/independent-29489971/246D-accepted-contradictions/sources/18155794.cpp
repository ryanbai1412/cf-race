#include<bits/stdc++.h>

using namespace std;

vector<int>v[100001];

set<int>c[100001];

int main()

{       

        int n,m,col[100005],i,mm=0;

        scanf("%d %d",&n,&m);

        for(i=1;i<=n;i++)

        {

                scanf("%d",&col[i]);

                c[i].insert(i);

                if(col[i]>mm)

                mm=col[i];

        }

        for(i=0;i<m;i++)

        {

                int a,b;

                scanf("%d %d",&a,&b);

                v[a].push_back(col[b]);

                v[b].push_back(col[a]);

        }

        for(i=1;i<=n;i++)

        {

                for(int j=0;j<v[i].size();j++)

                c[col[i]].insert(v[i][j]);      

        }

        int maa=0;

        for(i=1;i<=mm;i++)

        if(c[i].size()>c[maa].size())

        maa=i;

        if(c[maa].size()==1)

        {

                maa=10000000;

                for(i=1;i<=n;i++)

                if(col[i]<maa)

                maa=col[i];

          }

        printf("%d",maa);

        return 0;

}