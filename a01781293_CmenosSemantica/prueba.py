# A01781293 Santiago Tena
from globalTypes import *
from lexer import *

fileName = "prueba"
f = open(fileName + '.c-', 'r')
program = f.read()
f.close()
progLong = len(program)
program = program + '$'
position = 0

recibeScanner(program, position, progLong)

token, tokenString, _ = getToken()
while token != TokenType.ENDFILE:
    token, tokenString, _ = getToken()
