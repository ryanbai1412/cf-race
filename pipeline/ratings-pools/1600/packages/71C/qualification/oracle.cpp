#include"iostream"
#include<stdio.h>
using namespace std;
int a[110000];
int main()
{
    int i,j,k,n;
    while(scanf("%d",&n)!=EOF)
    {
        for(i=1;i<=n;i++)
            scanf("%d",&a[i]);
        a[i]=a[1];
        bool flag=false;
        for(i=1;i<=n/3;i++)
            if(n%i==0)
            {
                int T=i;

                for(j=1;j<1+i;j++)
                {
                    for(k=j;k<=n+1;k+=i)
                        if(!a[k])
                            break;
                    if(k>n+1)
                    {
                        flag=true;
                  //      cout<<i<<endl;
                        break;
                    }
                }
                if(flag)
                    break;
            }
        if(flag)
            puts("YES");
        else
            puts("NO");

    }
    return 0;
}