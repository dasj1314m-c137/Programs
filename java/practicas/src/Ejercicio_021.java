class Ejercicio_021 {
    public static void main(String[] args) {
        int x = 10;
        double opr_polinomio;

        opr_polinomio = Math.pow(x, 4) + Math.pow(x, 3) + (Math.pow(x, 2) / 2) - x;

        System.out.printf("%.2f", opr_polinomio);
    }
}