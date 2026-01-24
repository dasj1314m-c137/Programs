class Ejercicio_020 {
    public static void main(String[] args) {
        double x = 1.1, opr_polinomio;

        opr_polinomio = Math.pow(x, 4) + Math.pow(x, 3) + (2 * Math.pow(x, 2)) - x;
        System.out.printf("%.4f ",opr_polinomio);
    }
}