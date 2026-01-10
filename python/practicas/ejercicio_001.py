again = True

# creation of warning messajes
warning_type = "The input that you enter is incorrect, must be a whole number"
warning_size = "Your number si too big, the number must not pass 64"
warning_negative = "The number must be higher to 0"

# creation of function that calculates the max_value and creates the sequence
def calcular_maximo(bits):
    # we will calculate the max_value and sequence of the bits
    max_value = 2**bits - 1
    sequence = "1" * bits 
    return max_value, sequence      

# creation of while loop of the program
while again:
    # while loop that controls input user is safe
    while True:
        try:
            # the user input that should be a whole number(type int)
            print()
            bits = int(input("Inserte los bits: "))
            # prevent input 0 or negatives numbers
            if bits <= 0:
                print(warning_negative)
                continue
            # prevent big numbers and memory
            elif bits > 64:
                print(warning_size)
                continue
            # if is correct input, breaks and go out of the loop
            break
        # if the input is not of type number 
        except ValueError:
            print(warning_type)
        finally:
            print()

    # call to the function that makes all the operation
    max_value, sequence = calcular_maximo(bits)

    # print the result of max_value and sequence of bits
    print(f"The max value that can be represent with {bits} bits is: {max_value}, and its sequence is: {sequence}")
    print()

    # the user input that should be a string
    confirmation = input("Quieres hacer otra operacion (No/Si): ")


    try:
        if not "si" == confirmation.lower():
            again = False
            break
    except ValueError:
        print(warning_type)
            


    
