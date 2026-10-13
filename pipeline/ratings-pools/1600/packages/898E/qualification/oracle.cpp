#include <bits/stdc++.h>
using namespace std;

vector<int> sq;

bool is_square(int x)
{
    return x == (*lower_bound(sq.begin(), sq.end(), x));
}

int step_to_sq(int x)
{
    auto it = lower_bound(sq.begin(), sq.end(), x);
    int c1 = *it - x;
    it--;
    int c2 = x - *it;

    return min(c1, c2);
}

int main()
{
    for(int i=0; i*i<1010500500; i++) sq.push_back(i*i);

    int n; cin >> n;
    vector<int> A, B;
    int cnt = 0;
    for(int i=0; i<n; i++)
    {
        int x; cin >> x;
        if(is_square(x))
        {
            cnt += 1;
            A.push_back(x);
        }
        else
        {
            cnt -= 1;
            B.push_back(x);
        }
    }

    long long res = 0;
    if(cnt > 0)
    {
        cnt /= 2;
        vector<int> g;
        for(int i=0; i<A.size(); i++)
        {
            int cc = 0;
            while(is_square(A[i]))
            {
                A[i]++;
                cc++;
            }

            g.push_back(cc);
        }

        sort(g.begin(), g.end());
        for(int i=0; i<cnt;
         i++) res += g[i];
    }
    else if(cnt < 0)
    {
        cnt *= -1;
        cnt /= 2;
        vector<int> g;
        for(int i=0; i<B.size(); i++)
        {
            g.push_back(step_to_sq(B[i]));
        }

        sort(g.begin(), g.end());
        for(int i=0; i<cnt; i++) res += g[i];
    }

    cout << res << endl;

    return 0;
}