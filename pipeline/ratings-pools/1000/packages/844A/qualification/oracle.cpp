//Bismillahir Rahmanir Rahim
#include <bits/stdc++.h>
using namespace std;

typedef int LL;
typedef unsigned int LLU;
typedef vector<int> VI;
typedef vector<int> VLL;
typedef map<int, int> MAPII;
typedef map<string,int> MAPSI;
typedef pair<int, int> PII;
typedef pair<LL, LL> PLL;
typedef pair<double, double> PDD;

#define FOR(i,a,b) for(i=a;i<=b;i++)
#define ROF(i,a,b) for(i=a;i>=b;i--)
#define FR(i,n)    for(i=0;i<n;i++)
#define RF(i,n) for(i=n;i>0;i--)
#define CLR(a) memset ( a, 0, sizeof ( a ) )
#define RESET(a) memset ( a, -1, sizeof ( a ) )
#define PB(a)    push_back ( a )
#define X first
#define Y second
#define sf scanf
#define pf printf
#define pb push_back
#define mp make_pair

int main()
{
    int ar[26];
    for(int i=0;i<26;i++)
    {
        ar[i]=0;
    }
    char stringi[10000];
    scanf("%s", stringi);
    int p,l;
    cin>>p;
    l=strlen(stringi);
    if(l<p)
    {
        cout<<"impossible"<<endl;
    }
    else
    {
        for(int i=0;i<l;i++)
        {
            ar[stringi[i]-'a']++;
        }
//        for(int i=0;i<26;i++)
//        {
//            cout<<ar[i]<<endl;
//        }
        int count=0;
        for(int i=0;i<26;i++)
        {
            if(ar[i]>=1)
            {
                count++;
            }

        }
            if(count<p)
            {
                count=p-count;
            }
            else
            {
                count=0;
            }
            cout<<count<<endl;
    }
    return 0;
}