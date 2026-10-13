#include <cstdio>
#include <vector>
#include <cstring>
#include <algorithm>
#include <iostream>
#include <cmath>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <numeric>
#include <limits>
#include <string.h>

#define pb push_back
#define mp make_pair

using namespace std;
typedef long long LL;
#define DEBUG(x) cout << '>' << #x << ':' << x << endl;
#define imax numeric_limits<LL>::max()
#define imin numeric_limits<LL>::min()
#define lmax numeric_limits<LL>::max()
#define lmin numeric_limits<LL>::min()

LL oo =lmin;

LL Q = 1e9 + 7;

LL gcd(LL a, LL b)
{
    if (b == 0){
        return a;
    }
    return gcd(b, a%b);
}
/*

LL prime[10000002];
LL small[10000002];
// 0 == prime
// 1 == not prime
vector<LL> r;
void seive()
{
    memset (small, -1, sizeof(small));
    prime[0]=1;
    prime[1]=1;

    for (LL i=2;i*i<=300002;i++){
        if (prime[i] == 0){
            for (LL j=i*i; j <= 300002;j += i){
                prime[j]=1;
                if (small[j] == -1){
                    small[j] = i;
                }
            }
        }
    }
    for (LL i=0;i<=300002;i++){
        if (prime[i] == 0){
            r.push_back(i);
        }
    }
}




LL Q=1e9 + 7;

long long poww(LL a, LL b)
{
    long long x=1,y=a;
    while(b > 0)
    {
        if(b%2 == 1)
        {
            x=(x*y);
            if(x>Q) x%=Q;
        }
        y = (y*y);
        if(y>Q) y%=Q;
        b /= 2;
    }
    return x;
}
LL C[52][52];

void binomialCoeff()
{
    LL i, j;
    for (i = 0; i <= 50; i++)
    {
        for (j = 0; j <= 50; j++)
        {
            if (j == 0 || j == i)
                C[i][j] = 1;
            else
                C[i][j] = C[i-1][j-1] + C[i-1][j];
        }
    }
}
*/
LL p[100002];

int main()
{
    LL n;
    cin>>n;
    LL s=0;
    for (LL i=1;i<=n;i++){
        cin>>p[i];
        s += p[i];
    }
   // cout<<s<<"|n";
    LL t=s/n;
    LL ans=0;
    for (LL i=1;i<n;i++){
        if (p[i] < t){
            LL tt=abs(p[i] - t);
            ans += tt;
            p[i+1]-=tt;
        } else {
            LL tt=abs(p[i] - t);
            ans += tt;
            p[i+1]+=tt;
        }
      /*  for (LL i=1;i<=n;i++){
            cout<<p[i]<<" ";
        }
        cout<<"\n";*/

    }
    cout<<ans<<"\n";
    return 0;
}