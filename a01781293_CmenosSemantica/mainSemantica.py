from globalTypes import *
from parserCmenos import *
from semantica import *

def main():
    try:
        with open('prueba.c-', 'r') as f:
            program = f.read().strip()
        
        print("[MAIN] Archivo leído:")
        print("----- INICIO -----")
        print(program)
        print("----- FIN -----")
        print(f"Longitud: {len(program)} caracteres")
        
        program = program + '$'
        position = 0
        programLength = len(program)

        print("[MAIN] Programa con $:")
        print("----- INICIO -----")
        print(program)
        print("----- FIN -----")
        print(f"Nueva longitud: {programLength} caracteres")
        
        program = program + '$'
        position = 0
        programLength = len(program)

        from lexer import recibeScanner
        recibeScanner(program, position, programLength)

        AST, Error = parse(True)
        
        if not Error:
            print("\nÁrbol sintáctico:")
            printTree(AST)
            
            print("\nAnálisis semántico:")
            semantica(AST, True)
        else:
            print("\nErrores sintácticos detectados. No se realiza análisis semántico.")
            
    except FileNotFoundError:
        print("Error: No se encontró el archivo prueba.c-")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()