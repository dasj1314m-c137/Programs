import java.util.Scanner;
import java.util.ArrayList;

class Ejercicio_008 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ArrayList<Integer> list_nums = new ArrayList<>();
        String data;
        int suma_media = 0;
        double varianza, media, suma_varianza = 0;

        System.out.println("Ingrese sus datos separados por comas y le daremos la media");
        data = input.nextLine();

        for (String i: data.split(",")) {
            list_nums.add(Integer.parseInt(i));
        }
        for (int i: list_nums) {
            suma_media += i;
        }
        media = (double) suma_media / list_nums.size();

        for (int i: list_nums) {
            suma_varianza += Math.pow((i - media), 2);
        }
        varianza = suma_varianza / list_nums.size();

        String rdo = String.format("La varianza de los datos %s es: %.2f", data, varianza);
        System.out.println(rdo);
    }
}