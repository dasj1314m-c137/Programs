def es_palindromo(palabra: str) -> bool:
    """
    Verifica si una palabra es un palíndromo usando recursión.
    
    Restricciones cumplidas:
    - Sin bucles (for/while)
    - Sin slicing [::-1]
    - Sin funciones integradas como reversed()
    """
    # Caso base: cadena vacía o de 1 carácter es palíndromo
    if len(palabra) <= 1:
        return True
    
    # Comparar primer y último carácter
    if palabra[0] != palabra[-1]:
        return False
    
    # Llamada recursiva con la subcadena interior
    return es_palindromo(palabra[1:-1])


# Pruebas
if __name__ == "__main__":
    pruebas = [
        "radar",
        "anilina",
        "python",
        "oso",
        "reconocer",
        "hola",
        "a",
        ""
    ]
    
    for p in pruebas:
        print(f"'{p}': {es_palindromo(p)}")