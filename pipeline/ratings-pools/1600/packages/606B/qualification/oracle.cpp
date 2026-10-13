#include <stdio.h>
#include <string.h>

bool visit[501][501];

char s[100001];

int main() {
    int x, y, cx, cy;
    scanf("%d %d %d %d",&x,&y,&cx,&cy);
    scanf("%s",s);
    int l=strlen(s);
    int cnt=0;
    for(int i=0;i<l;i++) {
        if(visit[cx][cy]) printf("0 ");
        else {
            visit[cx][cy]=true;;
            printf("1 "); cnt++;
        }
        if(s[i]=='L') {
            if(cy>1) cy--;
        } else if(s[i]=='R') {
            if(cy<y) cy++;
        } else if(s[i]=='U') {
            if(cx>1) cx--;
        } else if(s[i]=='D') {
            if(cx<x) cx++;
        }
    }
    printf("%d",x*y-cnt);
}