#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <utility>
#include <vector>
#include <deque>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <string>
#include <cstring>
#include <cmath>
#include <climits>

using namespace std;

#define Ttran Pphu
#define pll pair <long long, long long>
#define null NULL
#define show(x) cout << #x << " = " << x << endl

long long n;
long long L[100100];
deque<long long> Q;
long long _result = 0;

int main () {
     cin >> n;
     for (long long i = 0; i < n; i++) {
          cin >> L[i];
     }
     sort (L, L+n);
     for (long long i = n-1; i >= 0; i--) {
          if (L[i-1] == L[i] - 1 || L[i-1] == L[i]) {
               Q.push_back (L[i-1]);
               i--;
          }
     }
     if (Q.size ()%2) {
          Q.pop_back ();
     }
     while (!Q.empty ()) {
          long long tmp = Q.front ();
          Q.pop_front ();
          _result += tmp * Q.front ();
          Q.pop_front ();
     }
     cout << _result;
}