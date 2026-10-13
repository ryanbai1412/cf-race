/*
ID: espr1t
TASK: 
KEYWORDS: 
*/

#include <cstdio>
#include <cstring>
#include <algorithm>

using namespace std;
FILE *in; FILE *out;

const int MAX = 131072;

struct Add {
    int type;
    int num, length, count;
    long long start, end;
};

int n, m;
Add a[MAX];
int nums[MAX];

long long scanLong(FILE* fp = stdin) {
    char buff[32];
    fscanf(fp, "%s", buff);
    int start = 0, len = (int)strlen(buff);
    bool sign = true;
    if (buff[0] == '-')
        sign = false, start = 1;
    long long val = 0;
    for (int i = start; i < len; i++)
        val = val * 10 + buff[i] - '0';
    return sign ? val : -val;
}

int main(void) {
	in = stdin; out = stdout;
//	in = fopen("A.in", "rt"); // out = fopen("file.out", "wt");
	
	long long len = 0;
	fscanf(in, "%d", &n);
	for (int i = 0; i < n; i++) {
	    fscanf(in, "%d", &a[i].type);
	    if (a[i].type == 1) {
	        fscanf(in, "%d", &a[i].num);
	        a[i].start = len;
	        a[i].end = len;
	        if (len < MAX)
	            nums[len] = a[i].num;
	        len++;
	    }
	    else {
	        fscanf(in, "%d %d", &a[i].length, &a[i].count);
	        a[i].start = len;
	        a[i].end = len + (long long)a[i].length * a[i].count - 1;
	        for (int c = 0; c < (long long)a[i].length * a[i].count; c++) {
	            if (len + c >= MAX) break;
	            nums[len + c] = nums[c % a[i].length];
	        }
	        len += (long long)a[i].length * a[i].count;
	    }
	}

	int numQueries;
	fscanf(in, "%d", &numQueries);
	for (int i = 0; i < numQueries; i++) {
	    long long q = scanLong(in) - 1;
	    int left = 0, right = n - 1;
	    int ans = -1;
	    while (left <= right) {
	        int mid = (left + right) / 2;
	        if (a[mid].start > q)
	            right = mid - 1;
	        else if (a[mid].end < q)
	            left = mid + 1;
	        else {
	            if (a[mid].type == 1) {
	                ans = a[mid].num;
	            }
	            else {
	                q -= a[mid].start;
	                q %= a[mid].length;
	                ans = nums[q];
	            }
	            break;
	        }
	    }
	    if (ans == -1)
	       fprintf(stderr, "Bad, sedlarov, bad!\n");
	    fprintf(out, "%d%c", ans, i + 1 == numQueries ? '\n' : ' ');
	}
	return 0;
}