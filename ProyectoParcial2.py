import re

#Funcion para armar la tabla de transicion
def imprimirtablatransicion():
    tabla = [
        ['Estado', 'a', 'b', '#', 'Otro'],
        ['0', '1', '-', '-', '-'],
        ['1', '1', '2', '-', '-'],
        ['2', '3', '2', '-', '-'],
        ['3', '3', '3', '4', '3'],
        ['4', '4', '4', '4', '4']
    ]

    print("Tabla de transición de estados:")
    for fila in tabla:
        print(' | '.join(f"{celda:^5}" for celda in fila))
        print('-' * 29)


#Patrón corregido que acepta espacios vacíos/otros caracteres como epsilon
patron = re.compile("(.*a)(.*b)(a)(b\2|a*\*)(#+|a\2|b\3)")
patron2 = re.compile("(a)(b)(a)(b\2|a)(#+|a\2|b\3)")
imprimirtablatransicion()
print("\nValidación de cadenas:")

try:
        with open("cadena.txt", 'r') as reader:
            for line in reader.readlines():
                cadena = line.strip()
                if re.fullmatch(patron, cadena):
                    print(cadena)
                    print('---Es válido---')
                    print()
                else:
                    print(cadena)
                    print('---No es válido---')
                    print()
        reader.close
except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo 'cadena.txt'.")
except IOError:
        print("Error: Hubo un problema al leer el archivo 'cadena.txt'.")

       
