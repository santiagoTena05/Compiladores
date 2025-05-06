# A01781293 Santiago Tena
from globalTypes import *
from parserCmenos import * # el Parser importa el Scanner

fileName = "prueba"
f = open(fileName + '.c-', 'r')
program = f.read()      # lee todo el archivo a compilar
f.close()               # cerrar el archivo con programa fuente
progLong = len(program) # longitud original del programa
program = program + '$' # agregar un caracter $ que represente EOF
position = 0            # posición del caracter actual del string

# Inicializar variables globales
Error = False
imprimeScanner = True  # Para ver los tokens que se van reconociendo

# Pasar los globales al scanner y parser
recibeScanner(program, position, progLong)
recibeParser(program, position, progLong)

# Iniciar el parsing
syntaxTree, Error = parse(True) # con True imprime el árbol