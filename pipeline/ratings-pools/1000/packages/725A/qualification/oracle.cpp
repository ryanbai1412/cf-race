#include <bits/stdc++.h>

using namespace std;
typedef long long int ll;

char s[200005];
int n;


int main()
{
    scanf("%d",&n);
    scanf("%s",s);
    int ans=0;
    for(int i=0;i<n;i++)
    {
        if(s[i]=='<')
            ans++;
        else
            break;
    }
    for(int i=n-1;i>=0;i--)
    {
        if(s[i]=='>')
            ans++;
        else
            break;
    }
    printf("%d\n",ans);

    return 0;
}