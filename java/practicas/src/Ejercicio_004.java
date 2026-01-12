import java.util.ArrayList;
import java.util.Scanner;
import java.util.Collections;

class Ejercicio_004 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String userNum, secuencia;
        ArrayList<String> secuencia_bits = new ArrayList<>();
        int cociente, residuo;
        boolean negativo = false;

        System.out.println("Ingresa el numero y te daremos su secuencia");
        userNum = input.nextLine();

        if (userNum.contains("-")) {
            userNum = userNum.replace("-", "");
            negativo = true;
        }
        cociente = Integer.parseInt(userNum);

        while (cociente != 0) {
            residuo = cociente % 2;
            secuencia_bits.add(Integer.toString(residuo));
            cociente = cociente / 2;
        }
        while (secuencia_bits.size() < 8) {
                secuencia_bits.add("0");
        }
        if (negativo) {
            for (int i=0; i<2; i++) {
                for (int j=0; j<8; j++) {
                    if (secuencia_bits.get(j).equals("1")) {
                        secuencia_bits.set(j, "0");
                    } else {
                        secuencia_bits.set(j, "1");
                        if (i == 1) {
                            break;
                        }
                    }
                }
            }
        }
        Collections.reverse(secuencia_bits);
        secuencia = String.join("", secuencia_bits);

        System.out.println(secuencia);
    }
}