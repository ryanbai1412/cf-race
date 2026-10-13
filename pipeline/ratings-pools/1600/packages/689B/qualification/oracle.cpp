#include <vector>
#include <cstdio>
#include <queue>

using namespace std;

int main() {
    int n;
    scanf("%d", &n);
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        scanf("%d", &(a[i]));
        --a[i];
    }
    vector<int> res(n, -1);
    res[0] = 0;
    queue<int> q;
    q.push(0);

    while (!q.empty()) {
        int cur = q.front();
        q.pop();

        if (cur + 1 < n && res[cur + 1] == -1) {
            res[cur + 1] = res[cur] + 1;
            q.push(cur + 1);
        }
        if (cur - 1 >= 0 && res[cur - 1] == -1) {
            res[cur - 1] = res[cur] + 1;
            q.push(cur - 1);
        }
        if (res[a[cur]] == -1) {
            res[a[cur]] = res[cur] + 1;
            q.push(a[cur]);
        }
    }

    for (int i = 0; i < n; ++i) {
        printf("%d ", res[i]);
    }
    printf("\n");

    return 0;
}