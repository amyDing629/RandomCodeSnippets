#include <stdio.h>
#include <stdlib.h>
int main(){
    char phone[11];
    scanf("%s", phone);
    int num;
    scanf("%d", &num);
    int rst = 0;
    if (num == -1){
        printf("%s\n", phone);
    }
    else if (num >= 0 && num <= 9){
        printf("%c\n", phone[num]);
    }
    else{
        printf("ERROR\n");
        rst = 1;
    }
    return rst;



}
