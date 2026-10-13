#include <bits/stdc++.h>

using namespace std;

int main(){
    int n,q;
    scanf("%d %d",&n,&q);

    map<int,int>M;
    for(int i=1,x;i<=n;i++){
        scanf("%d",&x);
        M[x]++;
    }
    while(q--){
        int x,ans=0;
        scanf("%d",&x);
        for(map<int,int>::reverse_iterator it=M.rbegin();it!=M.rend();it++){
            int key=it->first;
            int cnt=it->second;
            if(key<=x){
                int all=min(cnt,x/key);
                ans+=all;
                x-=all*key;
            }
        }
        if(x)printf("-1\n");
        else printf("%d\n",ans);
    }

    return 0;
}