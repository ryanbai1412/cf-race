#include <bits/stdc++.h>
using namespace std;

static string s;
static size_t p = 0;

[[noreturn]] static void bad() { exit(3); }

static long long readU(long long lo, long long hi) {
    size_t st = p;
    while (p < s.size() && s[p] >= '0' && s[p] <= '9') p++;
    size_t len = p - st;
    if (len == 0 || len > 10) bad();
    if (len > 1 && s[st] == '0') bad();
    long long v = 0;
    for (size_t i = st; i < p; i++) v = v * 10 + (s[i] - '0');
    if (v < lo || v > hi) bad();
    return v;
}

static void space() {
    if (p >= s.size() || s[p] != ' ') bad();
    p++;
}

static bool eol() {
    if (p < s.size() && s[p] == '\r') {
        p++;
        if (p >= s.size() || s[p] != '\n') bad();
        p++;
        return true;
    }
    if (p < s.size() && s[p] == '\n') {
        p++;
        return true;
    }
    return false;
}

int main() {
    {
        char buf[1 << 16];
        size_t r;
        while ((r = fread(buf, 1, sizeof buf, stdin)) > 0) s.append(buf, r);
    }
    int n = (int)readU(1, 1000000);
    if (!eol()) bad();
    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        if (i) space();
        a[i] = readU(0, 1000000000);
    }
    eol();
    if (p != s.size()) bad();
    long long alive = 0, reach = n;
    for (long long i = n - 1; i >= 0; i--) {
        if (i < reach) alive++;
        reach = min(reach, i - a[i]);
    }
    printf("%lld\n", alive);
    return 0;
}
