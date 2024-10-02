import re
from graphviz import Digraph

# Función para imprimir la tabla de transición
def imprimirtablatransicion():
    tabla = [
        ['Estado', 'a', 'b', '*', '#', 'Otro'],
        ['0', '1', '-', '-', '-', '-'],
        ['1', '-', '2', '-', '-', '-'],
        ['2', '3', '-', '-', '-', '-'],
        ['3', '3', '1', '4', '-', '-'],
        ['4', '3', '1', '-', '4', '-']
    ]
    print("Tabla de transición de estados:")
    for fila in tabla:
        print(' | '.join(f"{celda:^5}" for celda in fila))
    print('-' * 29)

# Genera tabla de frecuencia para imprimir
def generarTabla(mensaje):

    estado = '0'
    tabla = [['|||'],['|0|'],['|1|'],['|2|'],['|3|'],['|4|']]
    pasarG4 = False
    #Evalua el estado y actua de acuerdo al caracter leido y el estado
    for i in mensaje:
        i = "|" + i + "|"
        if estado == "0":
            tabla[0].append(i)
            if i == "|a|":
                tabla[1].append("|1|")
                estado = '1'
            else:
                tabla[1].append("|0|")

         
        
        elif estado == "1":
            tabla[0].append(i)
            if i == "|b|":
                tabla[2].append("|2|")
                estado = '2'
            else:
                tabla[2].append("|1|")


        elif estado == "2":

            tabla[0].append(i)
            estado = "3"
            

           
            tabla[3].append("|3|")
            

        elif estado == "3":
            tabla[0].append(i)
            if i == "|b|":
                tabla[4].append("|1|")
                estado = "1"
            elif i == "|a|":
                tabla[4].append("|3|")
                estado = "3"
            elif i == "|*|":
                tabla[4].append("|4|")
                estado = "4"
            

        elif estado == "4":
            tabla[0].append(i)
            if i == "|#|":
                tabla[5].append("|4|")
                estado = "4"
            elif i == "|a|":
                tabla[5].append("|1|")
                estado = "1"
            elif i == "|b|":
                tabla[5].append("|2|")
                estado = "2"
            
        for z in range (len(tabla)):
            if len(tabla[z]) < len(tabla[0]):
                tabla[z].append("|-|")

    for r in tabla:
        print(' '.join(map(str,r)))
# Función para obtener el siguiente estado según la tabla de transición
def obtener_siguiente_estado(estado_actual, caracter):
    tabla_transicion = {
        '0': {'a': '1'},
        '1': {'b': '2'},
        '2': {'a': '3'},
        '3': {'a': '3', 'b': '1', '*': '4'},
        '4': {'a': '3', 'b': '1', '#': '4'}
    }
    
    if estado_actual in tabla_transicion and caracter in tabla_transicion[estado_actual]:  # Verifica si el estado actual y el caracter están en la tabla de transición.
        return tabla_transicion[estado_actual][caracter] # Retorna el siguiente estado.
    else:
        return '4'  # Estado de error

# Función para generar el árbol de derivación
def generar_arbol_derivacion(cadena, numero):  # Crea un nuevo gráfico para el árbol de derivación
    dot = Digraph(comment=f'Árbol de Derivación - Cadena {numero}')
    dot.attr(rankdir='TB')  # Establece la dirección del gráfico de arriba hacia abajo (Top To Bottom)

    estado_actual = '0' # Comienza en el estado inicial
    for i, caracter in enumerate(cadena): # Itera sobre cada caracter de la cadena
        estado_siguiente = obtener_siguiente_estado(estado_actual, caracter) # Obtiene el siguiente estado

        # Se usa el mismo nodo si apunta a sí mismo
        if estado_siguiente == estado_actual:
            dot.node(f"{estado_actual}", estado_actual)  # Solo crea un nodo para el estado
            dot.edge(f"{estado_actual}", f"{estado_siguiente}", label=caracter)  # Muestra la transición
        else:
            dot.node(f"{estado_actual}", estado_actual)  # Crea un nodo para el estado actual
            dot.node(f"{estado_siguiente}", estado_siguiente)  # Crea un nodo para el siguiente estado
            dot.edge(f"{estado_actual}", f"{estado_siguiente}", label=caracter)  # Muestra la transición
        
        estado_actual = estado_siguiente # Actualiza el estado actual al siguiente estado.

    # Añadir colores a los nodos finales para el estado de aceptación
    if estado_actual == '4' and cadena[-1] == '#':
        dot.node(f"{estado_actual}", estado_actual, color='green', style='filled') #verde si se llega al estado de aceptación
    else:
        dot.node(f"{estado_actual}", estado_actual, color='red', style='filled') #Rojo si no se llega al estado de aceptación

    #  # Genera el archivo del árbol de derivación en formato PNG y limpia los archivos temporales que cera grapviz para renderizar la imagen.
    dot.render(f'arbol_derivacion_cadena_{numero}', format='png', cleanup=True)

patron = re.compile("(.*a)(.*b)(a)(b\2|a*\*)(#+|a\2|b\3)")

imprimirtablatransicion()
print("\nValidación de cadenas:")

try:
    with open("cadena.txt", 'r') as reader:
        for numero, line in enumerate(reader.readlines(), 1):
            cadena = line.strip()
            if re.fullmatch(patron, cadena):
                print(f"Cadena {numero}: {cadena}")
                print('---Es válido---')
                generar_arbol_derivacion(cadena, numero)  # Generar árbol
            else:
                print(f"Cadena {numero}: {cadena}")
                print('---No es válido---')
                generar_arbol_derivacion(cadena, numero)  # Generar árbol   
except FileNotFoundError:
    print("Error: No se pudo encontrar el archivo 'cadena.txt'.")
except IOError:
    print("Error: Hubo un problema al leer el archivo 'cadena.txt'.")
