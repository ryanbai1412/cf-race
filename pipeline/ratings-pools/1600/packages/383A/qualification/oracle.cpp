#include <stdio.h>
#include <iostream>
using namespace std;

typedef long long int64;

int main() {
  int n, k = 0;
  int64 ans = 0;
  scanf("%d", &n);
  for (int i = 0; i < n; i++) {
    int x;
    scanf("%d", &x);
    if (!x) {
      ans += k;
    } else {
      k++;
    }
  }
  cout << ans << endl;
  return 0;
}