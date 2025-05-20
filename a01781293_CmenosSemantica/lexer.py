# A01781293 Santiago Tena
from globalTypes import *

lineno = 1  # Número de línea
program = ""  
position = 0
programLength = 0

def recibeScanner(prog, pos, long):
    global program, position, programLength
    program = prog
    position = pos
    programLength = long


def reservedLookup(tokenString):
    for w in ReservedWords:
        if tokenString == w.value:
            return TokenType(w.value)
    return TokenType.ID

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
                state = StateType.INASSIGN
            elif c == '!':
                save = False
                state = StateType.INEXCL
            elif c == '<':
                state = StateType.INLT
            elif c == '>':
                state = StateType.INGT
            elif c == '/':
                if position + 1 < programLength and program[position+1] == '*':
                    save = False
                    position += 1
                    state = StateType.INCOMMENT
                else:
                    currentToken = TokenType.OVER
                    state = StateType.DONE
            elif c == '$':  # Caso especial para ENDFILE
                state = StateType.DONE
                currentToken = TokenType.ENDFILE
            elif c in '+-*;:,()[]{}':
                state = StateType.DONE
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
                    '}': TokenType.RBRACE
                }
                currentToken = token_map.get(c, TokenType.ERROR)
            elif c == '\n':
                lineno += 1
                save = False
            elif c in ' \t\r':
                save = False
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

        elif state == StateType.INASSIGN:
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