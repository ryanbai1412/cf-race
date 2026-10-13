#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef pair<int,int> ii;

int main(){

    int n;
    cin>>n;
    ll rez = -1000000000000;
    ll ar[n];
    for(int ctr1=0;ctr1<n;ctr1++)
        cin>>ar[ctr1];
    ll csum = 0;
    for(int ctr1=0;ctr1<n - 1;ctr1++){
        ll dif = abs(ar[ctr1]-ar[ctr1+1]);
        if(ctr1&1)
            dif = -dif;
        csum += dif;
        rez = max(rez, csum);
        if (csum < 0)
            csum = 0;
    }
    csum = 0;
    for(int ctr1=0;ctr1<n - 1;ctr1++){
        ll dif = abs(ar[ctr1]-ar[ctr1+1]);
        if(!(ctr1&1))
            dif = -dif;
        csum += dif;
        rez = max(rez, csum);
        if (csum < 0)
            csum = 0;
    }
    cout<<rez;
    return 0;
}