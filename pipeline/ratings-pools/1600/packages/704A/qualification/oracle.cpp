#include <cstdio>
#include <string>
#include <cstring>
#include <cstdint>
#include <climits>
#include <numeric>
#include <functional>
#include <algorithm>
#include <vector>
#include <set>
#include <map>
#include <queue>

using namespace std;

int main() {
  int n, q;
  scanf("%d%d", &n, &q);
  vector<bool> read;
  int total_read = 0;
  map<int, vector<int>> app2no;
  int lt = 0;
  for (int i = 0; i < q; i++) {
    int a, b;
    scanf("%d%d", &a, &b);
    if (a == 1) {
      app2no[b].push_back(read.size());
      read.push_back(false);
    }
    else if (a == 2) {
      for (auto c : app2no[b]) {
        if (!read[c])
          total_read++;
        read[c] = true;
      }
      app2no[b].clear();
    }
    else if (a == 3) {
      for (int j = lt; j < b; j++) {
        if (!read[j])
          total_read++;
        read[j] = true;
      }
      lt = max(lt, b);
    }
    int ans = read.size() - total_read;
    printf("%d\n", ans);
  }
  return 0;
}