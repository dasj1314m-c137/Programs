import java.util.Scanner;

class Ejercicio_009 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        double radio, area;

        System.out.println("Ingrese el radio del circulo y le daremos su area");
        radio = input.nextDouble();
        area = 3.1416 * Math.pow(radio, 2);

        System.out.printf("El area del circulo es %.4f²\n", area);
    }
}
