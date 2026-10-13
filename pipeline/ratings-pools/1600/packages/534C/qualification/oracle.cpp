#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    ios::sync_with_stdio(0);
    ll n,s;
    cin >> n >> s;
    vector <int> nums(n);
    ll sum = 0;
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
        sum+= nums[i];
    }
    for (int i = 0; i < n; i++) {
        ll val = sum-nums[i];
        ll res = max(0LL,s-val-1);
        res+= max(nums[i]-(s-(n-1)),0LL);
        cout << res;
        if (i != n-1)
            cout << " ";
    }
    return 0;
}