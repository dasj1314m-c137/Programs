#include <stdio.h>

int main(void) {
    printf("Estos son los numeros impares del 1 al 15\n");
    for (int i=1; i<16; i++) {
        if (i % 2 == 0) continue;
        printf("%d\n", i);
    }
    return 0;
}
