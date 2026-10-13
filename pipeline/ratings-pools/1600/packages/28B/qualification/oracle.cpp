#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <queue>
#include <stack>
#include <set>
#include <map>

using namespace std;


bool a[150][150];
int comps [150];
vector< vector<int> > vcomps;
bool used[150];

int main()
{
	int n;
	int i,j;
	cin>>n;
	int nums[150];
	for(i=0;i<n;++i)
		cin>>nums[i];

	int deg[150];
	for(i=0;i<n;++i)
		cin>>deg[i];

	for(i=0;i<n;++i)
	{
		if(i-deg[i] >= 0)
		{
			a[i][i-deg[i]] = true;
			a[i-deg[i]][i] = true;
		}
		if(i+deg[i] < n)
		{
			a[i][i+deg[i]] = true;
			a[i+deg[i]][i] = true;
		}
	}
	int x;

	for(i=0;i<n;++i)
		if(!used[i])
		{
			vector<int> tmp;
			
			queue<int> q;
			q.push(i);
			used[i] = true;
			while(!q.empty())
			{
				x = q.front();
				tmp.push_back(x);
				q.pop();
				for(j=0;j<n;++j)
					if(!used[j] && a[x][j])
					{
						used[j] = true;
						q.push(j);
					}
			}
			vcomps.push_back(tmp);
			int k = vcomps.size();
			int kk = tmp.size();
			for(j=0;j<kk;++j)
				comps[ tmp[j] ] = k-1;
		}
	
	for(i=0;i<n;++i)
	{
		int k = nums[i] - 1;
		int vs = comps[k];
		int vsz = vcomps[vs].size();
		for(j=0;j<vsz;++j)
			if(vcomps[vs][j] == i)
				break;
		if(j==vsz)
		{
			cout<<"NO\n";
			return 0;
		}
	}
	cout<<"YES\n";
	return 0;
}