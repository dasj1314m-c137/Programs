import java.util.Scanner;

class Ejercicio_002 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        int bits, userNum;
        double valor_maximo;
        String inputUser, rdo;

        System.out.println("Ingrese un numero y te dire con cuantos bits se representa");
        inputUser = input.nextLine();

        bits = 1;
        valor_maximo = 1;
        userNum = Integer.parseInt(inputUser);

        while (userNum > valor_maximo) {
            bits += 1;
            valor_maximo = Math.round(Math.pow(2, bits)) - 1;
        }
        rdo = String.format("El numero %d se puede representar con %d bits", userNum, bits);
        System.out.println(rdo);
    }
}