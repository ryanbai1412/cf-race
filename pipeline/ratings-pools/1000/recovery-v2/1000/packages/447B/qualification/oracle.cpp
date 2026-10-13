#include <bits/stdc++.h>



using namespace std;



int a[101];

int main() {

    string s;

    int n, c=0, mx=0;

    cin>>s>>n;

    for (int i=1; i<=26; ++i){

        cin>>a[i];

        mx = max(mx, a[i]);

    }

    for (int j=0; j<s.size(); ++j){

        c+=(j+1)*(a[s[j]-96]);

    }

    for (int i=s.size()+1; i<=n+s.size(); ++i){

        c+=i*mx;

    }

    cout<<c;



    return 0;

}