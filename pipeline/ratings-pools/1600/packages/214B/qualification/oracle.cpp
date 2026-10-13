#include<iostream>
using namespace std;

int cnt[15];

void output()
{
    int i,j;
    for(i=9;i>=0;i--)
        if(cnt[i])
            break;
    if(i==0) cnt[i]=1;
    for(i=9;i>=0;i--)
        for(j=0;j<cnt[i];j++)
            cout<<i;
    cout<<endl;
}

int main()
{
    int i,j,n,s,x,f;
    cin>>n;
    s=0;
    for(i=0;i<n;i++)
    {
        cin>>x;
        cnt[x]++;
        s+=x;
        //cout<<s<<endl;
    }
    if(!cnt[0])
    {
        cout<<-1<<endl;
        return 0;
    }
    else
    {
        if(s%3==0)
        {
            output();
        }
        else if(s%3==1)
        {
            for(i=1;i<=9;i+=3)
                if(cnt[i])
                {
                    cnt[i]--;
                    break;
                }
            if(i<=9)
            {
                output();
            }
            else
            {
                int c=0;
                for(i=2;i<=9;i+=3)
                {
                    if(cnt[i])
                    {
                        cnt[i]--,c++;
                        if(c==2) break;
                        if(cnt[i])
                            cnt[i]--,c++;
                        if(c==2) break;
                    }
                }
                output();
            }
        }
        else if(s%3==2)
        {
            for(i=2;i<=9;i+=3)
                if(cnt[i])
                {
                    cnt[i]--;
                    break;
                }
            if(i<=9)
            {
                output();
            }
            else
            {
                int c=0;
                for(i=1;i<=9;i+=3)
                {
                    if(cnt[i])
                    {
                        cnt[i]--,c++;
                        if(c==2) break;
                        if(cnt[i])
                            cnt[i]--,c++;
                        if(c==2) break;
                    }
                }
                output();
            }
        }
    }
    return 0;
}