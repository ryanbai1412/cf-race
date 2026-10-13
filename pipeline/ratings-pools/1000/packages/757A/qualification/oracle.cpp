#include<map>
#include<set>
#include<queue>
#include<string>
#include<vector>
#include<cstring>
#include<iostream>
using namespace std;
int main()
{
    string s="Bulbasaur";
    int a[1000]={0};
    for(int i=0;i<s.size();i++)
        a[s[i]]++;
    string t;
    cin>>t;
    int b[1000]={0};
    for(int i=0;i<t.size();i++)
        b[t[i]]++;
    int ret=1e9+1e9;
    for(int i=0;i<256;i++)
        if(a[i])
        {
            ret=min(ret,b[i]/a[i]);
        }
    cout<<ret<<endl;
}