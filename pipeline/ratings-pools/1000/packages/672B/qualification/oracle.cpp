#include<iostream>

#include<stdio.h>

#include<string.h>

#include<algorithm>

using namespace std;

bool k[210];

int main()

{

	int n;

	memset(k,false,sizeof(k));

	int c=0;

	scanf("%d",&n);

	for (int i=1;i<=n;i++){

		char ch=getchar();

		while (!(ch>='a' && ch<='z')) ch=getchar();

		if (!k[ch]) k[ch]=true;

		else c++;

	}

	if (n>26) printf("-1\n"); else printf("%d\n",c);

}