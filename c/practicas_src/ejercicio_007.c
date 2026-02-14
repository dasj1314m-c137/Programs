#include <stdio.h>

int main(void) {
    int nums[] = {10, 20, 30, 40};
    int size_arr_nums = 4;

    printf("Estos son los elementos del array\n");
    for (int i=0; i < size_arr_nums; i++) {
        printf("%d\n", nums[i]);
    }
    return 0;
}
