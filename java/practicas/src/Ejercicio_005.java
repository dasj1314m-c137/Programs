import java.util.Collections;
import java.util.Scanner;
import java.util.ArrayList;

class Ejercicio_005 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String userInput;
        ArrayList<Integer> nums = new ArrayList<>();
        String[] oprs = {"+", "-"};
        boolean preNegative = false, resta = false;
        int rdo;

        System.out.println("Ingresa la operacion y te daremos el resultado en secuencia binaria de 8 bits");
        userInput = input.nextLine();

        if (userInput.contains("-")) {
            resta = true;
            if (userInput.startsWith("-") && userInput.contains("+")) {
                preNegative = true;
            }
        }
        for (String opr: oprs) {
            userInput = userInput.replace(opr, " ");
        }
        for (String str_num: userInput.split(" ")) {
            if (str_num.isEmpty()) {
                continue;
            }
            nums.add(Integer.parseInt(str_num));
        }
        if (preNegative) {
            rdo = nums.get(1) - nums.get(0);
        } else if (resta) {
            rdo = nums.get(0) - nums.get(1);
        } else {
            rdo = nums.get(0) + nums.get(1);
        }

        String secuencia, userNum = Integer.toString(rdo);
        ArrayList<String> secuencia_bits = new ArrayList<>();
        int cociente, residuo;
        boolean negativo = false;

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