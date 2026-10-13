#include <bits/stdc++.h>
using namespace std;

static void fail(const string& msg) {
    fprintf(stderr, "INVALID: %s\n", msg.c_str());
    exit(1);
}

static vector<string> splitTokens(const string& s) {
    vector<string> r;
    size_t i = 0;
    while (i < s.size()) {
        while (i < s.size() && s[i] == ' ') i++;
        if (i >= s.size()) break;
        size_t j = i;
        while (j < s.size() && s[j] != ' ') j++;
        r.push_back(s.substr(i, j - i));
        i = j;
    }
    return r;
}

static long long toInt(const string& t, long long lo, long long hi, const char* name) {
    if (t.empty() || t.size() > 18) fail(string("bad integer for ") + name);
    if (t.size() > 1 && t[0] == '0') fail(string("leading zero in ") + name);
    for (char c : t) if (c < '0' || c > '9') fail(string("bad integer for ") + name);
    long long v = stoll(t);
    if (v < lo || v > hi) fail(string(name) + " out of range");
    return v;
}

int main() {
    std::ios::sync_with_stdio(false);
    string data((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
    vector<string> lines;
    {
        size_t st = 0;
        while (true) {
            size_t p = data.find('\n', st);
            string l = data.substr(st, p == string::npos ? string::npos : p - st);
            while (!l.empty() && (l.back() == ' ' || l.back() == '\t' || l.back() == '\r')) l.pop_back();
            lines.push_back(l);
            if (p == string::npos) break;
            st = p + 1;
        }
        while (!lines.empty() && lines.back().empty()) lines.pop_back();
        for (auto& l : lines) {
            if (l.empty()) fail("empty line");
            for (char c : l) if (c == '\r' || c == '\t' || (unsigned char)c >= 128) fail("bad character");
        }
    }
    if (lines.empty()) fail("empty input");
    vector<string> h = splitTokens(lines[0]);
    if (h.size() != 2) fail("line 1 must have 2 tokens");
    int n = (int)toInt(h[0], 2, 2500, "n");
    int m = (int)toInt(h[1], 2, 2500, "m");
    if ((int)lines.size() != n + 1) fail("wrong number of lines");
    vector<int> P((size_t)(n + 1) * (m + 1), 0);
    auto at = [&](int i, int j) -> int& { return P[(size_t)i * (m + 1) + j]; };
    for (int i = 0; i < n; i++) {
        vector<string> t = splitTokens(lines[i + 1]);
        if (t.size() != 1) fail("grid line must be one token");
        const string& row = t[0];
        if ((int)row.size() != m) fail("grid row length mismatch");
        int run = 0;
        for (int j = 0; j < m; j++) {
            char c = row[j];
            if (c != '0' && c != '1') fail("grid char must be 0/1");
            run += c - '0';
            at(i + 1, j + 1) = at(i, j + 1) + run;
        }
    }
    long long best = LLONG_MAX;
    int K = max(n, m);
    for (int k = 2; k <= K; k++) {
        long long kk = (long long)k * k;
        long long cost = 0;
        for (int r0 = 0; r0 < n && cost < best; r0 += k) {
            int r1 = min(r0 + k, n);
            for (int c0 = 0; c0 < m; c0 += k) {
                int c1 = min(c0 + k, m);
                long long ones = at(r1, c1) - at(r0, c1) - at(r1, c0) + at(r0, c0);
                cost += min(ones, kk - ones);
            }
        }
        best = min(best, cost);
    }
    printf("%lld\n", best);
    return 0;
}
