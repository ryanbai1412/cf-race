#include <bits/stdc++.h>
using namespace std;

struct Reader {
    string data;
    size_t position = 0;

    explicit Reader(string raw) {
        data.reserve(raw.size());
        for (size_t i = 0; i < raw.size(); ++i) {
            if (raw[i] == '\r') {
                if (i + 1 >= raw.size() || raw[i + 1] != '\n') throw 3;
            } else {
                data.push_back(raw[i]);
            }
        }
    }

    vector<int> integers(int count, int low, int high) {
        if (position == data.size()) throw 3;
        size_t end = data.find('\n', position);
        if (end == string::npos) end = data.size();
        vector<int> result;
        while (position < end) {
            char c = data[position];
            if (c == ' ' || c == '\t') {
                ++position;
                continue;
            }
            bool negative = false;
            if (c == '+' || c == '-') {
                negative = c == '-';
                ++position;
            }
            if (position == end || data[position] < '0' || data[position] > '9') throw 3;
            int value = 0;
            while (position < end && data[position] >= '0' && data[position] <= '9') {
                value = value * 10 + data[position++] - '0';
                if (value > 1000) throw 3;
            }
            if (position < end && data[position] != ' ' && data[position] != '\t') throw 3;
            if (negative) value = -value;
            if (value < low || value > high) throw 3;
            result.push_back(value);
            if ((int)result.size() > count) throw 3;
        }
        position = end == data.size() ? end : end + 1;
        if ((int)result.size() != count) throw 3;
        return result;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    try {
        Reader p(string(istreambuf_iterator<char>(cin), {}));
        auto header = p.integers(2, 1, 1000);
        int n = header[0], m = header[1];
        vector<unsigned char> grid(n * m);
        vector<int> first_row(n, m), last_row(n, -1), first_column(m, n), last_column(m, -1);
        bool actor = false;
        for (int r = 0; r < n; ++r) {
            auto values = p.integers(m, 0, 1);
            for (int c = 0; c < m; ++c) {
                grid[r * m + c] = values[c];
                if (values[c]) {
                    actor = true;
                    first_row[r] = min(first_row[r], c);
                    last_row[r] = c;
                    first_column[c] = min(first_column[c], r);
                    last_column[c] = r;
                }
            }
        }
        if (!actor || p.position != p.data.size()) throw 3;
        int answer = 0;
        for (int r = 0; r < n; ++r) {
            for (int c = 0; c < m; ++c) {
                if (!grid[r * m + c]) {
                    answer += first_row[r] < c;
                    answer += last_row[r] > c;
                    answer += first_column[c] < r;
                    answer += last_column[c] > r;
                }
            }
        }
        cout << answer << '\n';
    } catch (...) {
        return 3;
    }
}
