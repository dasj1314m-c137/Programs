import java.util.Scanner;
import java.util.ArrayList;

class Ejercicio_007 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ArrayList<Integer> list_nums = new ArrayList<>();
        String data;
        int suma = 0;
        double media;

        System.out.println("Ingrese sus datos separados por comas y le daremos la media");
        data = input.nextLine();

        for (String i: data.split(",")) {
            list_nums.add(Integer.parseInt(i));
        }
        for (int i: list_nums) {
            suma += i;
        }
        media = (double) suma / list_nums.size();

        String rdo = String.format("La media de los datos %s es: %.2f", data, media);
        System.out.println(rdo);
    }
}