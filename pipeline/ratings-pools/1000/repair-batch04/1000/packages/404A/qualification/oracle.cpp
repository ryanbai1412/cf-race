#include<iostream>
using namespace std;

int N;
string x[305];

int main(){
    cin >> N;
    for(int i=0; i<N; i++)
        cin >> x[i];
        
    char a = x[0][0];
    char b = x[0][1];
    
    if(a == b){ cout << "NO" << endl; return 0; }
    
    bool good = true;
    
    for(int i=0; i<N; i++)
        for(int j=0; j<N; j++)
            if(i==j || i+j == N-1) good &= x[i][j]==a;
            else good &= x[i][j]==b;
            
    if(good) cout << "YES" << endl;
    else cout << "NO" << endl;
    return 0;
}