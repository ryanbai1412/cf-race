#include <bits/stdc++.h>
using namespace std;

typedef long long i64;

map <i64, set <int>> mp;
set <i64> values;

void add_nr(i64 val, i64 poz)
{
    mp[val].insert(poz);
    if (mp[val].size() == 2)
        values.insert(val);
}

void rem_first_2(i64 val)
{
    mp[val].erase(mp[val].begin());
    int poz = *mp[val].begin();
    mp[val].erase(poz);
    if (mp[val].size() < 2)
        values.erase(val);
    add_nr(2 * val, poz);
}

map <int, i64> ans;

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int n, c;
    cin >> n;

    for (int i(1); i <= n; i++) {
        cin >> c;
        add_nr(c, i);
    }

    while (!values.empty()) {
        i64 x = *values.begin();
        rem_first_2(x);
    }

    for (auto i : mp) {
        for (auto j : i.second)
            ans[j] = i.first;
    }

    cout << ans.size() << '\n';

    for (auto i : ans)
        cout << i.second << ' ';

    return 0;
}