#include <iostream>

#include <bits/stdc++.h>



using namespace std;



int main()

{

    int a[100000];

    int n,k;

    cin >> n >> k;

    for(int i = 0 ; i < n ; i++) cin >> a[i];



    int talk = ceil(((double)sqrt(1+1LL*8*k)-1.0)/2.0)-1;



    cout << a[k-(1LL*talk*(1+talk)/2)-1];



    return 0;

}