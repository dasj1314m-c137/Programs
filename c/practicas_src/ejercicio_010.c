/*
📌 Contexto
Estás programando un sistema que decide si un usuario puede acceder o no según varias condiciones combinadas.

🎯 Reglas del sistema
El usuario debe ingresar:

Edad (entero)
Código de acceso (entero)
Cantidad de intentos previos fallidos (entero)
Modo administrador (0 = no, 1 = sí)

❌ El acceso se deniega si:

Edad < 18 Y no es administrador
Intentos fallidos ≥ 3 Y no es administrador
Código incorrecto Y no es administrador

(Sí, el admin es el comodín… como en la vida real)
*/

#include <stdio.h>

int main(void) {
    int intentos = 3;
    int edad, clave, admin = 0;
    char es_admin;

    while (intentos >= 1) {

        printf("\nEres administrador? (s/n): "); scanf(" %c", &es_admin);
        if (es_admin == 's') admin = 1;
        if (admin) { printf("\nAcceso concedido\n"); break; }

        printf("Ingresa tu edad: "); scanf("%d", &edad);
        printf("Ingresa el codigo de acceso: "); scanf("%d", &clave);

        if (edad >= 18 && clave == 1234) { printf("\nAcceso concedido\n"); break; }
        intentos--;
        printf("\nAcceso denegado te quedan %d intentos\n", intentos);
    }
    return 0;
}
