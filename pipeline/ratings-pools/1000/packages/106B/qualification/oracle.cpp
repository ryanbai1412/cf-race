#include <iostream>

#include <cstdio>

using namespace std;



bool outdate[110];

main()

{

    int n , pr[110] , spe[110] , ram[110] , hdd[110];

    cin>>n;



    for(int i=0 ; i<n; i++)

        cin>>spe[i]>>ram[i]>>hdd[i]>>pr[i];



    for(int i=0 ; i<n ; i++)

    {

        for(int j=0 ; j<n ; j++)

        {

            if(spe[i] < spe[j] && ram[i] < ram[j] && hdd[i] < hdd[j])

                outdate[i] = 1;

        }

    }

    int mi = -1 , mini = 1100;



    for(int i=0 ; i<n ; i++)

    {

        if(!outdate[i])

        {

            if(pr[i]<mini)

                mini = pr[i] , mi = i;

        }

    }



    cout<<mi+1<<endl;



}