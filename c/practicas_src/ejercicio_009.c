#include <stdio.h>

int factorial(int num) {
    int producto = 1;
    for (int i=num; i>=1; i--) {
        producto = producto * i;
    }
    return producto;
}

int main(void) {
    int num;
    printf("Ingresa un numero y obten su factorial\n");
    scanf("%d", &num);

    int factorial_num = factorial(num);
    printf("El factorial es: %d\n", factorial_num);

    return 0;
}
