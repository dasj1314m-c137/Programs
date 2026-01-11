import java.util.Scanner;

class Ejercicio_003 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String seq1, seq2;
        int rdo_sum = 0;

        System.out.println("Este programa suma dos secuencias binarias que pases acontinuacion");
        System.out.println("Ingrese la primera secuencia binaria: ");
        seq1 = input.nextLine();
        System.out.println("Ingrese la segunda secuencia binaria: ");
        seq2 = input.nextLine();

        String[] sequences = {seq1, seq2};

        for (String seq: sequences) {
            String reversed = new StringBuilder(seq).reverse().toString();
            for (int i=0; i < reversed.length(); i++) {
                if (reversed.charAt(i) == '1') {
                    rdo_sum += (int)Math.pow(2, i);
                }
            }
        }
        System.out.println("El resultado de la suma de ambas secuencias binarias es: "+rdo_sum);
    }
}