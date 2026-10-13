#include <cstdio>

#include <cstring>



const int N=100000+5;



char s[N];

int n;



int main() {

	scanf("%s", s);

	n=strlen(s);

	printf("%s", s);

	for(int i=n-1; i>=0; --i) putchar(s[i]);

	putchar('\n');

	return 0;

}