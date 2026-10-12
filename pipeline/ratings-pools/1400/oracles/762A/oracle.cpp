#include <bits/stdc++.h>
using namespace std;

void require(bool condition, const string& reason) {
    if (!condition) throw runtime_error(reason);
}

vector<string> read_lines(size_t expected) {
    string raw((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
    string normalized;
    for (size_t i = 0; i < raw.size(); ++i) {
        if (raw[i] == '\r') {
            require(i + 1 < raw.size() && raw[i + 1] == '\n', "bare carriage return");
            ++i;
            normalized += '\n';
        } else normalized += raw[i];
    }
    vector<string> lines;
    size_t start = 0;
    for (size_t i = 0; i < normalized.size(); ++i) {
        if (normalized[i] == '\n') {
            lines.push_back(normalized.substr(start, i - start));
            start = i + 1;
        }
    }
    lines.push_back(normalized.substr(start));
    while (!lines.empty() && lines.back().find_first_not_of(" \t") == string::npos)
        lines.pop_back();
    require(lines.size() == expected, "wrong line count");
    return lines;
}

vector<long long> integers(const string& line, size_t expected, long long low, long long high) {
    vector<long long> result;
    size_t i = 0;
    while (i < line.size()) {
        if (line[i] == ' ' || line[i] == '\t') { ++i; continue; }
        bool negative = false;
        if (line[i] == '+' || line[i] == '-') {
            negative = line[i] == '-';
            ++i;
        }
        require(i < line.size() && line[i] >= '0' && line[i] <= '9', "invalid integer");
        long long value = 0;
        while (i < line.size() && line[i] >= '0' && line[i] <= '9') {
            int digit = line[i++] - '0';
            require(value <= (LLONG_MAX - digit) / 10, "integer overflow");
            value = value * 10 + digit;
        }
        require(i == line.size() || line[i] == ' ' || line[i] == '\t', "invalid integer");
        if (negative) value = -value;
        require(low <= value && value <= high, "integer out of range");
        result.push_back(value);
    }
    require(result.size() == expected, "wrong token count");
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    try {
        auto lines = read_lines(1);
        auto values = integers(lines[0], 2, 1, 1000000000000000LL);
        long long n = values[0], k = values[1];
        require(k <= 1000000000LL, "k out of range");
        vector<long long> smaller, larger;
        for (long long d = 1; d <= n / d; ++d) {
            if (n % d == 0) {
                smaller.push_back(d);
                if (d != n / d) larger.push_back(n / d);
            }
        }
        long long count = smaller.size() + larger.size();
        if (k > count) cout << "-1\n";
        else if (k <= (long long)smaller.size()) cout << smaller[k - 1] << '\n';
        else cout << larger[count - k] << '\n';
    } catch (const exception& error) {
        cerr << error.what() << '\n';
        return 1;
    }
}
