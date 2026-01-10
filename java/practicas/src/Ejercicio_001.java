// importar Scanner para poder esperar entrada de usuario
import java.util.Scanner;
// creation of principal class main()
class Ejercicio_001 {
    public static void main(String[] args) {
        // creation of the object Scanner to receive input
        Scanner input = new Scanner(System.in);

        // creation of variables to manage values
        boolean again = true;
        int bits, max_value;
        String sequence, confirmation, inputUser;
        
        // creation of warning messages
        String warning_size = "Your number is too big, the number must not pass 64";
        String warning_type = "Your input is incorrect, you have to pass a whole number";
        String warning_negative = "The number must be higher to 0";

        while (again) {
            // now we ask for the input user, that should be the number of bits and inside the while loop we check it
            while (true) {
                // use try to cacth an exception if the input's type is incorrect
                try {
                    // ask for the bits
                    System.out.println("Inserte el numero de bits: ");
                    inputUser = input.nextLine();
                    // checks that input user is not an empty value
                    if (inputUser.isEmpty()) {
                        System.out.println(warning_type);
                    } else {
                        bits = Integer.parseInt(inputUser);
                        // checks the number is higher than 0
                        if (bits <= 0) {
                            System.out.println(warning_negative);
                            continue;
                        }
                        // checks the number is less than 64
                        else if (bits > 64) {
                            System.out.println(warning_size);
                            continue;
                        }
                        break;
                    }
                }
                // capturing the exception for incorrect type
                catch (NumberFormatException e) {
                    System.out.println(warning_type);
                } finally {
                    System.out.println();
                }
            }
            // we calculate the max_value and the sequence here
            max_value = (1 << bits) - 1;
            sequence = "1".repeat(bits);

            // print the result of the value_max and the sequence of the bits
            String msj = String.format("The max value that can be represented with %d bits is: %d, and its sequence is: %s", bits, max_value, sequence);
            System.out.println(msj);
            System.out.println();

            // ask user to do or don't do another operation
            System.out.println("Quiere hacer otra operacion (No/Si)");
            confirmation = input.nextLine();

            // checks input and if not "si" main while loop ends
            if (!("si".equalsIgnoreCase(confirmation))) {
                again = false;
            }
        }
    }
}