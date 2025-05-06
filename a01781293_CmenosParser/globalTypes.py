# A01781293 Santiago Tena
from enum import Enum

class TokenType(Enum):
    ENDFILE = 300
    ERROR = 301

    # Palabras reservadas
    IF = 'if'
    VOID = 'void'
    ELSE = 'else'
    INT = 'int'
    RETURN = 'return'
    WHILE = 'while'
    
    # Tokens de multicaracteres
    ID = 310
    NUM = 311

    # Símbolos especiales
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    OVER = '/'
    LT = '<'
    LTEQ = '<='
    GT = '>'
    GTEQ = '>='
    EQ = '=='
    NEQ = '!='
    ASSIGN = '='
    SEMI = ';'
    COMMA = ','
    LPAREN = '('
    RPAREN = ')'
    LBRACK = '['
    RBRACK = ']'
    LBRACE = '{'
    RBRACE = '}'

# Estados del DFA
class StateType(Enum):
    START = 0
    INNUM = 1
    INID = 2
    INASSIGN = 3
    INLT = 4
    INGT = 5
    INEQ = 6
    INEXCL = 7
    INCOMMENT = 8
    OUTCOMMENT = 9
    DONE = 10

# Palabras reservadas
class ReservedWords(Enum):
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'

#***********   Syntax tree for parsing ************

class NodeKind(Enum):
    StmtK = 0
    ExpK = 1

class StmtKind(Enum):
    IfK = 0            # if (exp) stmt [else stmt]
    WhileK = 1         # while (exp) stmt
    AssignK = 2        # asignaciones x = y
    ReturnK = 3        # return [exp];
    VarDeclK = 4       # declaración de variable: int x;
    FunDeclK = 5       # declaración de función: int f() { }
    CompoundK = 6      # bloque de sentencias { }
    ExpressionK = 7    # expresión como sentencia sola: exp;
    EmptyK = 8         # una sentencia vacía ; sola (opcional, pero útil si quieres diferenciar)
    SelectK = 9 
    IterK = 10

class ExpKind(Enum):
    OpK = 0        # operación (aritmética o relacional)
    ConstK = 1     # constante (NUM)
    IdK = 2        # identificador (ID)
    CallK = 3      # llamada a función (ID(args))
    AssignK = 4    # asignación (ID = exp)
    CompareK = 5    # comparación (exp1 < exp2)
    AddK = 6       # suma (exp1 + exp2)
    MulK = 7       # multiplicación (exp1 * exp2)



class ExpType(Enum):
    Void = 0
    Integer = 1
    Boolean = 2


MAXCHILDREN = 4

class TreeNode:
    def __init__(self):
        self.child = [None] * MAXCHILDREN
        self.sibling = None
        self.lineno = 0
        self.nodekind = None
        self.stmt = None
        self.exp = None
        self.op = None
        self.val = None
        self.name = None
        self.type = None