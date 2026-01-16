import java.util.Scanner;

class Ejercicio_010 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int precio, suma_IVA, precio_IVA;

        System.out.println("Ingresa el precio y calcularemos su precio con IVA");
        precio = input.nextInt();
        suma_IVA = (16 * precio) / 100;
        precio_IVA = precio + suma_IVA;
        System.out.printf("El precio %d con IVA es: %d", precio, precio_IVA);
    }
}