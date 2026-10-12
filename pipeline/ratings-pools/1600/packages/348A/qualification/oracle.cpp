#include<algorithm>
#include<cmath>
#include<cstdio>
#include<cstring>
#include<iostream>
#include<map>
#include<queue>
#include<set>
#include<sstream>
#include<string>
#include<vector>

#define forn(i,n) for(int i=0;i<(int)n;i++)
#define dforn(i,n) for(int i=(int)n-1;i>=0;i--)
#define all(v) v.begin(),v.end()

using namespace std;

vector<long long> vec;

bool sePuede(long long k)
{
    long long t = 0;
    forn(i,vec.size())
        t += k-vec[i];
    if(t>=k)
        return true;
    return false;
}

int main()
{
    int n;
    cin >> n;
    vec.resize(n);
    forn(i,n)
        cin >> vec[i];
    sort(all(vec));
    reverse(all(vec));
    long long mn = vec[0]-1, mx = vec[0]*n;
    while(mx-mn>1)
    {
        long long k = (mx+mn)/2;
        if(sePuede(k)==true)
            mx = k;
        else
            mn = k;
    }
    cout << mx << endl;

}