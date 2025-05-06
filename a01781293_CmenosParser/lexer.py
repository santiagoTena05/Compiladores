# A01781293 Santiago Tena
from globalTypes import *

lineno = 1 # Número de línea

# Recibe un programa como una cadena de texto, la posición y longitud total
def recibeScanner(prog, pos, long):
    global program
    global position
    global programLength
    program = prog
    position = pos
    programLength = long

# Revisar si el ID identificado se encuentra en la clase de palabras reservadas
def reservedLookup(tokenString):
    for w in ReservedWords:
        if tokenString == w.value:
            return TokenType(w.value)  # Devuelve el TokenType correspondiente
    return TokenType.ID

# recibe una bandera booleana imprime , con valor por defecto true
def getToken(imprime=True):
    global position, lineno
    tokenString = ""
    currentToken = None
    state = StateType.START
    save = True

    while state != StateType.DONE:
        if position >= programLength:
            currentToken = TokenType.ENDFILE  
            tokenString = ""
            break

        c = program[position]
        save = True

        if state == StateType.START:
            if c.isdigit():
                state = StateType.INNUM
            elif c.isalpha():
                state = StateType.INID
            elif c == '=':
                state = StateType.INEQ
            elif c == '!':
                save = False
                state = StateType.INEXCL
            elif c == '<':
                state = StateType.INLT
            elif c == '>':
                state = StateType.INGT
            elif c == '/':
                if position + 1 < programLength and program[position+1] == '*': # Revisar si despues de un / existe un *
                    save = False
                    position += 1
                    state = StateType.INCOMMENT
                else:
                    currentToken = TokenType.OVER
                    state = StateType.DONE
            elif c in '+-*;:,()[]{}':
                state = StateType.DONE
                # Simbolos especiales
                token_map = {
                    '+': TokenType.PLUS,
                    '-': TokenType.MINUS,
                    '*': TokenType.TIMES,
                    ';': TokenType.SEMI,
                    ',': TokenType.COMMA,
                    '(': TokenType.LPAREN,
                    ')': TokenType.RPAREN,
                    '[': TokenType.LBRACK,
                    ']': TokenType.RBRACK,
                    '{': TokenType.LBRACE,
                    '}': TokenType.RBRACE,
                }
                currentToken = token_map.get(c, TokenType.ERROR)
            elif c == '\n':
                lineno += 1 # Aumentar uno a la linea
                save = False
            elif c in ' \t\r':
                save = False # Ignorar los tabs y los espacios y los enter
            else:
                currentToken = TokenType.ERROR
                state = StateType.DONE

        elif state == StateType.INNUM:
            if not c.isdigit():
                position -= 1
                save = False
                currentToken = TokenType.NUM
                state = StateType.DONE

        elif state == StateType.INID:
            if not c.isalnum():
                position -= 1
                save = False
                currentToken = reservedLookup(tokenString)
                state = StateType.DONE

        elif state == StateType.INEQ:
            if position + 1 < programLength and program[position+1] == '=':
                position += 1
                tokenString += '='
                currentToken = TokenType.EQ
            else:
                currentToken = TokenType.ASSIGN
            state = StateType.DONE

        elif state == StateType.INEXCL:
            if position + 1 < programLength and program[position+1] == '=':
                position += 1
                tokenString = "!="
                currentToken = TokenType.NEQ
            else:
                tokenString = "!"
                currentToken = TokenType.ERROR
            state = StateType.DONE

        elif state == StateType.INLT:
            if position + 1 < programLength and program[position+1] == '=':
                position += 1
                tokenString += '='
                currentToken = TokenType.LTEQ
            else:
                currentToken = TokenType.LT
            state = StateType.DONE

        elif state == StateType.INGT:
            if position + 1 < programLength and program[position+1] == '=':
                position += 1
                tokenString += '='
                currentToken = TokenType.GTEQ
            else:
                currentToken = TokenType.GT
            state = StateType.DONE

        elif state == StateType.INCOMMENT:
            save = False
            if c == '*' and position + 1 < programLength and program[position+1] == '/':
                position += 1
                state = StateType.START
            elif c == '\n':
                lineno += 1

        position += 1
        if save:
            tokenString += c

    if imprime:
        print(lineno, currentToken, ':', tokenString)
    return currentToken, tokenString, lineno
