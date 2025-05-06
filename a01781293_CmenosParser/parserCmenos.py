# A01781293 Santiago Tena
from globalTypes import *
from lexer import *

token = None # holds current token
tokenString = None # holds the token string value 
Error = False
tokenActual = None

#lineno = 1
SintaxTree = None
imprimeScanner = False

def syntaxError(message):
    global Error
    print(">>> Syntax error at line " + str(lineno) + ": " + message, end='')
    Error = True

def match(expected):
    global token, tokenString, lineno
    if (token == expected):
        token, tokenString, lineno = getToken(imprimeScanner)
        #print("TOKEN:", token, lineno)
    else:
        syntaxError("unexpected token -> ")
        printToken(token,tokenString)
        print("      ")
#-----------Producciones-------------------

#1. declaration-list —> { declaration }
def declaration_list():
    t = declaration()
    p = t
    while token in {TokenType.INT, TokenType.VOID}:
        q = declaration()
        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q
    return t

#2. declaration —> var-declaration | fun-declaration
def declaration():
    global token, tokenString
    #print(f"DEBUG - declaration() called with token: {token}, tokenString: {tokenString}")  # Línea nueva para depuración
    t = None
    if token in {TokenType.INT, TokenType.VOID}:
        tipo = type_specifier()
        if token == TokenType.ID:
            name = tokenString
            match(TokenType.ID)
            if token == TokenType.LPAREN:
                t = fun_declaration(tipo, name)
            elif token == TokenType.SEMI or token == TokenType.LBRACK:
                t = var_declaration(tipo, name)
            else:
                syntaxError("unexpected token after identifier")
        else:
            syntaxError("expected identifier after type")
    else:
        syntaxError("unexpected token at start of declaration")
    return t
#4. var-declaration —> type-specifier ID (";" | "[" NUM "]" ";")
def var_declaration(tipo, name):
    t = newStmtNode(StmtKind.VarDeclK)
    t.name = name
    t.type = tipo

    if token == TokenType.SEMI:
        match(TokenType.SEMI)
    elif token == TokenType.LBRACK:
        match(TokenType.LBRACK)
        if token == TokenType.NUM:
            t.val = int(tokenString)  # Guardamos el tamaño del arreglo
            match(TokenType.NUM)
        else:
            syntaxError("expected number inside brackets")
        match(TokenType.RBRACK)
        match(TokenType.SEMI)
    else:
        syntaxError("unexpected token in variable declaration")
    
    return t


#5. type-specifier —> "int" | "void"
def type_specifier():
    if token == TokenType.INT:
        match(TokenType.INT)
        return ExpType.Integer
    elif token == TokenType.VOID:
        match(TokenType.VOID)
        return ExpType.Void
    else:
        syntaxError("expected type specifier")
        return ExpType.Void

#6. fun-declaration —> type-specifier ID "(" params ")" compound-stmt
def fun_declaration(tipo, name):
    t = newStmtNode(StmtKind.FunDeclK)
    t.name = name
    t.type = tipo

    match(TokenType.LPAREN)
    # De momento, no procesamos params (lo harás después)
    # Podrías hacer aquí una mini versión de params() que no haga nada.
    params()
    match(TokenType.RPAREN)

    # Y tampoco procesamos bien el cuerpo compuesto aún:
    t.child[0] = compound_stmt()

    return t

#7. params —> param-list | "void"
def params():
    if token == TokenType.VOID:
        match(TokenType.VOID)
        if token == TokenType.ID:
            # Es una lista de parámetros que empieza con "void" mal usado (ej: void x)
            param_list()
        else:
            # Solo void: función sin parámetros
            return None
    else:
        return param_list()

# 8. param-list —> param { "," param }

def param_list():
    t = param()
    p = t
    while token == TokenType.COMMA:
        match(TokenType.COMMA)
        q = param()
        if p is not None:
            p.sibling = q
            p = q
    return t

#9. param —> type-specifier ID [ "[" "]" ]
def param():
    tipo = type_specifier()
    if token == TokenType.ID:
        name = tokenString
        match(TokenType.ID)
    else:
        syntaxError("Expected identifier in parameter")
        name = ""

    t = newStmtNode(StmtKind.VarDeclK)
    t.type = tipo
    t.name = name

    if token == TokenType.LBRACK:
        match(TokenType.LBRACK)
        match(TokenType.RBRACK)
        # Es un arreglo (no hacemos nada especial aquí salvo saberlo)

    return t

#10. compound-stmt —> "{" local-declarations statement-list "}"

def compound_stmt():
    match(TokenType.LBRACE)  # match "{"
    
    t = newStmtNode(StmtKind.CompoundK)  # Creamos nodo de tipo Compound Statement
    
    t.child[0] = local_declarations()    # Primer hijo: declaraciones locales
    t.child[1] = statement_list()         # Segundo hijo: lista de sentencias
    
    match(TokenType.RBRACE)  # match "}"
    
    return t

#11. local-declarations —> { var-declaration }
def local_declarations():
    global tokenActual
    t = None
    while tokenActual is not None and (tokenActual.tipo == TokenType.INT or tokenActual.tipo == TokenType.VOID):
        tipo = tokenActual.lexema
        match(tokenActual.tipo)
        if tokenActual.tipo != TokenType.ID:
            syntaxError("Expected identifier in local declaration")
            break
        name = tokenActual.lexema
        match(TokenType.ID)
        q = var_declaration(tipo, name)
        if t is None:
            t = q
            p = t
        else:
            p.sibling = q
            p = q
    return t

#12. statement-list —> { statement }
def statement_list():
    t = None  # Primer nodo
    p = None  # Nodo actual para construir la lista

    # Mientras el token sea válido para empezar un "statement"
    while token in {TokenType.IF, TokenType.WHILE, TokenType.RETURN, 
                    TokenType.ID, TokenType.NUM, TokenType.LPAREN, 
                    TokenType.LBRACE, TokenType.SEMI}:
        q = statement()  # Parseamos un "statement"
        
        if t is None:
            t = p = q  # Primer nodo
        else:
            p.sibling = q  # Conectamos el siguiente nodo
            p = q  # Nos movemos

    return t

#13. statement —> expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
def statement():
    global token, tokenString, lineno  # Añadir esta línea
    if token == TokenType.IF:
        return selection_stmt()
    elif token == TokenType.WHILE:
        return iteration_stmt()
    elif token == TokenType.RETURN:
        return return_stmt()
    elif token == TokenType.LBRACE:
        return compound_stmt()
    elif token in {TokenType.ID, TokenType.NUM, TokenType.LPAREN, TokenType.SEMI}:
        return expression_stmt()
    else:
        syntaxError("Unexpected token at start of statement")
        return None
#15. selection-stmt —> "if" "(" expression ")" statement | "if" "(" expression ")" statement "else" statement
def selection_stmt():
    t = newStmtNode(StmtKind.IfK)
    match(TokenType.IF)
    match(TokenType.LPAREN)
    t.child[0] = expression()   # Condición del if
    match(TokenType.RPAREN)
    t.child[1] = statement()    # Statement en caso verdadero
    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        t.child[2] = statement()  # Statement en caso falso (else)
    return t

#16. iteration-stmt —> "while" "(" expression ")" statement
def iteration_stmt():
    t = newStmtNode(StmtKind.WhileK)
    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    t.child[0] = expression()  # Condición del while
    match(TokenType.RPAREN)
    t.child[1] = statement()   # Cuerpo del while
    return t

#17. return-stmt —> "return" [expression] ";"
def return_stmt():
    global token, tokenString, lineno
    t = newStmtNode(StmtKind.ReturnK)
    match(TokenType.RETURN)
    
    if token != TokenType.SEMI:
        expr = expression()
        if expr is not None:
            t.child[0] = expr
    
    match(TokenType.SEMI)
    return t
#14. expression-stmt —> expression ";" | ";"
def expression_stmt():
    if token == TokenType.SEMI:
        match(TokenType.SEMI)
        t = newStmtNode(StmtKind.EmptyK)  # Es un statement vacío ";"
        return t
    else:
        t = expression()  # Procesa una expresión
        match(TokenType.SEMI)
        stmt = newStmtNode(StmtKind.ExpressionK)  # Nodo para expression-stmt
        stmt.child[0] = t
        return stmt

#18. expression —> var "=" expression | simple-expression
def expression():
    if token == TokenType.ID:
        name = tokenString
        match(TokenType.ID)
        if token == TokenType.ASSIGN or token == TokenType.LBRACK:
            v = var(name)
            if token == TokenType.ASSIGN:
                t = newExpNode(ExpKind.AssignK)
                t.child[0] = v
                match(TokenType.ASSIGN)
                t.child[1] = expression()
                return t
            else:
                return v
        else:
            savedName = name
            t = newExpNode(ExpKind.IdK)
            t.name = savedName
            return simple_expression(t)
    else:
        return simple_expression(None)

#19. var —> ID [ "[" expression "]" ]
def var(name):
    t = newExpNode(ExpKind.IdK)
    t.name = name
    if token == TokenType.LBRACK:
        match(TokenType.LBRACK)
        t.child[0] = expression()
        match(TokenType.RBRACK)
    return t

#20. simple-expression —> additive-expression [ relop additive-expression ]
def simple_expression(left=None):
    if left is None:
        t = additive_expression()
    else:
        t = left

    if token in {TokenType.LTEQ, TokenType.LT, TokenType.GT, TokenType.GTEQ, TokenType.EQ, TokenType.NEQ}:
        p = newExpNode(ExpKind.CompareK)
        p.child[0] = t
        p.op = token
        match(token)
        p.child[1] = additive_expression()
        t = p
    return t

#22. additive-expression —> term { addop term }
def additive_expression():
    t = term()
    while token in {TokenType.PLUS, TokenType.MINUS}:
        p = newExpNode(ExpKind.OpK)
        p.op = token
        p.child[0] = t
        match(token)
        p.child[1] = term()
        t = p
    return t

#23. addop —> "+" | "-"
def addop():
    if token == TokenType.PLUS:
        op = token
        match(TokenType.PLUS)
        return op
    elif token == TokenType.MINUS:
        op = token
        match(TokenType.MINUS)
        return op
    else:
        syntaxError("Expected '+' or '-'")
        return TokenType.ERROR

#24. term —> factor { mulop factor }
def term():
    t = factor()
    while token in {TokenType.TIMES, TokenType.OVER}:
        p = newExpNode(ExpKind.OpK)
        p.op = token
        p.child[0] = t
        match(token)
        p.child[1] = factor()
        t = p
    return t

#25. mulop —> "*" | "/"
def mulop():
    if token == TokenType.TIMES:
        op = token
        match(TokenType.TIMES)
        return op
    elif token == TokenType.OVER:
        op = token
        match(TokenType.OVER)
        return op
    else:
        syntaxError("Expected '*' or '/'")
        return TokenType.ERROR

#26. factor —> "(" expression ")" | var | call | NUM
def factor():
    global token, tokenString, lineno
    t = newExpNode(ExpKind.ConstK)  # Crear el nodo primero
    
    if token == TokenType.LPAREN:
        match(TokenType.LPAREN)
        t = expression()
        match(TokenType.RPAREN)
    elif token == TokenType.ID:
        name = tokenString
        match(TokenType.ID)
        if token == TokenType.LPAREN:
            t = call(name)
        else:
            t = var(name)
    elif token == TokenType.NUM:
        t.exp = ExpKind.ConstK  # Asegurar el tipo correcto
        t.val = int(tokenString)
        match(TokenType.NUM)
    else:
        syntaxError("Unexpected token in factor")
        token, tokenString, lineno = getToken(imprimeScanner)
        return None
    
    return t
#27. call —> ID "(" args ")"
def call(name):
    t = newExpNode(ExpKind.CallK)
    t.name = name
    match(TokenType.LPAREN)
    t.child[0] = args()
    match(TokenType.RPAREN)
    return t
#28. args —> arg-list | ε
def args():
    # Si el primer token no es un paréntesis de cierre, procesamos los argumentos
    if tokenActual.tipo != TokenType.RIGHT_PAREN:
        return arg_list()  # Procesamos los argumentos
    else:
        return []  # Si está vacío, retornamos una lista vacía

#29. arg-list —> expression { "," expression }
def arg_list():
    args = [expression()]  # Procesamos el primer argumento como una expresión
    
    # Mientras haya comas, seguimos procesando más expresiones
    while tokenActual.tipo == TokenType.COMMA:
        match()  # Consumimos la coma
        args.append(expression())  # Procesamos el siguiente argumento
    
    return args

def newStmtNode(kind):
    t = TreeNode();
    if (t==None):
        print("Out of memory error at line " + lineno)
    else:
        #for i in range(MAXCHILDREN):
        #    t.child[i] = None
        #t.sibling = None
        t.nodekind = NodeKind.StmtK
        t.stmt = kind
        t.lineno = lineno
    return t

# Function newExpNode creates a new expression 
# node for syntax tree construction

def newExpNode(kind):
    t = TreeNode()
    if t is None:
        print("Out of memory error at line", lineno)
    else:
        t.nodekind = NodeKind.ExpK
        t.exp = kind
        t.lineno = lineno
        t.type = ExpType.Void
        # Inicializar los hijos
        for i in range(MAXCHILDREN):
            t.child[i] = None
        t.sibling = None
    return t

def printToken(token, tokenString):
    if token in {TokenType.ELSE, TokenType.IF, TokenType.INT, TokenType.RETURN, TokenType.VOID, TokenType.WHILE}:
        print("Reserved word: ", tokenString)
    elif token == TokenType.LTEQ:
        print("Relop: <=")
    elif token == TokenType.LT:
        print("Relop: <")
    elif token == TokenType.GT:
        print("Relop: >")
    elif token == TokenType.GTEQ:
        print("Relop: >=")
    elif token == TokenType.EQ:
        print("Relop: ==")
    elif token == TokenType.NEQ:
        print("Relop: !=")
    elif token == TokenType.PLUS:
        print("Operator: +")
    elif token == TokenType.MINUS:
        print("Operator: -")
    elif token == TokenType.TIMES:
        print("Operator: *")
    elif token == TokenType.OVER:
        print("Operator: /")
    elif token == TokenType.ASSIGN:
        print("Operator: =")
    elif token == TokenType.SEMI:
        print("Symbol: ;")
    elif token == TokenType.COMMA:
        print("Symbol: ,")
    elif token == TokenType.LPAREN:
        print("Symbol: (")
    elif token == TokenType.RPAREN:
        print("Symbol: )")
    elif token == TokenType.LBRACK:
        print("Symbol: [")
    elif token == TokenType.RBRACK:
        print("Symbol: ]")
    elif token == TokenType.LBRACE:
        print("Symbol: {")
    elif token == TokenType.RBRACE:
        print("Symbol: }")
    elif token == TokenType.NUM:
      print("NUM, val= " + tokenString)
    elif token == TokenType.ID:
        print("ID, name= " + tokenString)
    else:
        print("Unknown token: ", tokenString)
        print("Token: ", token)
        print("TokenString: ", tokenString)
        print("Line number: ", lineno)
        print("Error in printToken")
        exit(1)  

# Variable indentno is used by printTree to
# store current number of spaces to indent
indentno = 0

# printSpaces indents by printing spaces */
def printSpaces():
    print(' ' * indentno, end='')

def printTree(tree):
    global indentno
    indentno += 2  # INDENT
    while tree is not None:
        printSpaces()
        if tree.nodekind == NodeKind.StmtK:
            if tree.stmt == StmtKind.IfK:
                print(f"{tree.lineno}: if")
            elif tree.stmt == StmtKind.WhileK:
                print(f"{tree.lineno}: While")
            elif tree.stmt == StmtKind.AssignK:
                print(f"{tree.lineno}: Assign to: {tree.name}")
            elif tree.stmt == StmtKind.ReturnK:
                print(f"{tree.lineno}: Return")
            elif tree.stmt == StmtKind.VarDeclK:
                print(f"{tree.lineno}: Variable Declaration: {tree.name}")
            elif tree.stmt == StmtKind.FunDeclK:
                print(f"{tree.lineno}: Function Declaration: {tree.name}")
            elif tree.stmt == StmtKind.CompoundK:
                print(f"{tree.lineno}: Compound Statement")
            elif tree.stmt == StmtKind.ExpressionK:
                print(f"{tree.lineno}: Expression Statement")
            elif tree.stmt == StmtKind.EmptyK:
                print(f"{tree.lineno}: Empty Statement")
            elif tree.stmt == StmtKind.SelectK:
                print(f"{tree.lineno}: Select Statement")
            elif tree.stmt == StmtKind.IterK:
                print(f"{tree.lineno}: Iteration Statement")
            else:
                print(f"{tree.lineno}: Unknown Statement Node")
        
        elif tree.nodekind == NodeKind.ExpK:
            if tree.exp == ExpKind.OpK:
                print(f"{tree.lineno}: Operator: ", end="")
                print(tree.op.value)
            elif tree.exp == ExpKind.ConstK:
                print(f"{tree.lineno}: Constant: {tree.val}")
            elif tree.exp == ExpKind.IdK:
                print(f"{tree.lineno}: Identifier: {tree.name}")
            elif tree.exp == ExpKind.CallK:
                print(f"{tree.lineno}: Function Call: {tree.name}")
            elif tree.exp == ExpKind.AssignK:
                print(f"{tree.lineno}: Assignment Expression to: {tree.name}")
            elif tree.exp == ExpKind.CompareK:
                print(f"{tree.lineno}: Comparison Expression")
            elif tree.exp == ExpKind.AddK:
                print(f"{tree.lineno}: Addition Expression")
            elif tree.exp == ExpKind.MulK:
                print(f"{tree.lineno}: Multiplication Expression")
            else:
                print(f"{tree.lineno}: Unknown Expression Node")
        
        else:
            print(f"{tree.lineno}: Unknown Node Kind")
        
        # Recorremos todos los hijos
        for i in range(MAXCHILDREN):
            printTree(tree.child[i])
        
        # Pasamos al hermano
        tree = tree.sibling
    indentno -= 2  # UNINDENT

def parse(imprime = True):
    global token, tokenString, lineno, imprimeScanner
    imprimeScanner = imprime  # Para que el scanner imprima si el parser imprime
    token, tokenString, lineno = getToken(imprimeScanner)
    t = declaration_list()
    if (token != TokenType.ENDFILE):
        syntaxError("Code ends before file\n")
    if imprime:
        printTree(t)
    return t, Error

def recibeParser(prog, pos, long): # Recibe los globales del main
    recibeScanner(prog, pos, long) # Para mandar los globales
