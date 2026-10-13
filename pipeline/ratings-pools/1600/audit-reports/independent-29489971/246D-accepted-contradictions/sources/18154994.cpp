/*

._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._

	ABHINANDAN AGARWAL

	MNNIT ALLAHABAD

	CSE

._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._

*/

/*

	Bina ek bhi WA ke saath kab submit hoga.. ? 

*/

#include<bits/stdc++.h>

using namespace std;

#define pc putchar_unlocked

#define gc getchar_unlocked

typedef long long ll;

typedef unsigned long long llu;

#define mp make_pair

#define pb push_back

#define sc(x) scanf("%d",&x)

#define sc2(x,y) scanf("%d%d",&x,&y)

#define sc3(x,y,z) scanf("%d%d%d",&x,&y,&z)

#define scstr(x) scanf("%s",x)

#define pd(x) printf("%d",x)

#define pstr(x) printf("%s",x)

#define newl() printf("\n")

#define fl(i,n) for (i=0;i<n;i++)

#define fle(i,n) for (i=1;i<=n;i++)

#define fla(i,a,n) for (i=a;i<n;i++)

#define mem(a,i) memset(a,i,sizeof(a))

#define fi first

#define se second

typedef pair<int,int> pii;

typedef pair<int,pair<int,int> > piii ;

#define wl(n) while (n--)

#define debug(x) cout<<"debug->"<<#x<<"::"<<x<<endl

#define debug2(x,y) cout<<#x<<" :: "<<x<<"\t"<<#y<<" :: "<<y<<"\n"

#define debug3(x,y,z) cout<<#x<<" :: "<<x<<"\t"<<#y<<" :: "<<y<<"\t"<<#z<<" :: "<<z<<"\n"

#define tr(container, it)  for(typeof(container.begin()) it = container.begin(); it != container.end(); it++) 

#define all(v) v.begin(),v.end()

const double eps=0.000000000000001 ;

#define MOD 1000000007

//-------------

int n,m;

int A[100010];

set<int> cor[100010];

int main()

{

	sc2(n,m);

	int i,j;

	int mx=0,ele=INT_MAX;

	for (i=1;i<=n;i++)

	{

		sc(A[i]);

		ele=min(A[i],ele);

		mx=max(mx,A[i]);

	}

	//printf("ele prebuilt is ::%d\n",ele);	

	for (i=0;i<m;i++)

	{

		int x,y;

		sc2(x,y);

		if (A[x]!=A[y])

		{

			cor[A[x]].insert(A[y]);

			cor[A[y]].insert(A[x]);

		}

	}

	int mxx=1;

	for (i=1;i<=mx;i++)

	{

		//printf("size of color %d is %lu\n",i,cor[i].size());

		if (cor[i].size()>0)

		{

			if (cor[i].size()>mxx)

			{

				ele=i;

				mxx=cor[i].size();

			}

			else if (cor[i].size()==mxx)

			{

				ele=min(ele,i);

			}

		}

	}

	//printf("mxx ::%d\n",mxx);

	printf("%d\n",ele);

	return 0;



}