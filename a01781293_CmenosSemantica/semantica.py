# A01781293 Santiago Tena
from globalTypes import *
from parserCmenos import *

class SymbolInfo:
    def __init__(self, name, tipo, lineno, kind, location):
        self.name = name
        self.tipo = tipo
        self.lineno = lineno
        self.kind = kind
        self.location = location

    def __repr__(self):
        type_name = self.tipo.name if hasattr(self.tipo, 'name') else str(self.tipo)
        return f"{self.name:<10} {self.kind:<8} {type_name:<10} {self.location:<8} {self.lineno}"

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.children = []
        self.next_location = 0

    def insert(self, name, info):
        if name in self.symbols:
            return False
        self.symbols[name] = info
        return True

    def lookup(self, name):
        return self.symbols.get(name, None)

    def __str__(self):
        lines = ["Name       Kind     Type       Location Line"]
        lines.append("-" * 45)
        for sym in self.symbols.values():
            lines.append(str(sym))
        return "\n".join(lines)

tablas = []

def tabla(tree, imprime=True):
    tablas.clear()
    global_tabla = SymbolTable()
    tablas.append(global_tabla)
    _buildSymbolTable(tree, global_tabla)
    
    if imprime:
        for i, tabla in enumerate(tablas):
            print(f"\nTabla de símbolos #{i + 1}:")
            print(tabla)
            if i > 0 and not tabla.symbols:
                print("  (Ámbito vacío - la función no tiene variables/parámetros declarados)")
    
    return tablas

def _buildSymbolTable(tree, current_scope):
    """Construye la tabla de símbolos recursivamente a partir del AST"""
    if tree is None:
        return

    # Caso 1: Declaración de función
    if tree.nodekind == NodeKind.StmtK and tree.stmt == StmtKind.FunDeclK:
        # Verificar si la función ya fue declarada
        if current_scope.lookup(tree.name):
            print(f"Error semántico (línea {tree.lineno}): Función '{tree.name}' ya declarada")
        else:
            # Insertar función en el ámbito actual
            func_info = SymbolInfo(
                name=tree.name,
                tipo=tree.type,
                lineno=tree.lineno,
                kind="Func",
                location=current_scope.next_location
            )
            current_scope.insert(tree.name, func_info)
            current_scope.next_location += 1

            # Crear nuevo ámbito para la función
            function_scope = SymbolTable(parent=current_scope)
            current_scope.children.append(function_scope)
            tablas.append(function_scope)

            # Procesar parámetros (si existen)
            param_node = tree.child[0]  # child[0] contiene los parámetros
            while param_node is not None:
                if (param_node.nodekind == NodeKind.StmtK and 
                    param_node.stmt == StmtKind.VarDeclK):
                    param_node.is_param = True  # Marcar como parámetro
                param_node = param_node.sibling

            _buildSymbolTable(tree.child[0], function_scope)  # Procesar parámetros
            _buildSymbolTable(tree.child[1], function_scope)  # Procesar cuerpo de función
        return

    # Caso 2: Declaración de variable/parámetro
    elif tree.nodekind == NodeKind.StmtK and tree.stmt == StmtKind.VarDeclK:
        kind = "Param" if hasattr(tree, 'is_param') and tree.is_param else "Var"
        
        # Verificar redeclaración en el mismo ámbito
        if current_scope.lookup(tree.name):
            print(f"Error semántico (línea {tree.lineno}): Redeclaración de variable '{tree.name}'")
        else:
            var_info = SymbolInfo(
                name=tree.name,
                tipo=tree.type,
                lineno=tree.lineno,
                kind=kind,
                location=current_scope.next_location
            )
            current_scope.insert(tree.name, var_info)
            current_scope.next_location += 1

    # Caso 3: Bloque compuesto (nuevo ámbito léxico)
    elif tree.nodekind == NodeKind.StmtK and tree.stmt == StmtKind.CompoundK:
        # Crear nuevo ámbito para el bloque
        block_scope = SymbolTable(parent=current_scope)
        current_scope.children.append(block_scope)
        tablas.append(block_scope)

        # Procesar declaraciones locales y sentencias en el nuevo ámbito
        _buildSymbolTable(tree.child[0], block_scope)  # Declaraciones locales
        _buildSymbolTable(tree.child[1], block_scope)  # Sentencias
        return

    # Caso 4: Sentencia return - verificar tipo de retorno
    elif tree.nodekind == NodeKind.StmtK and tree.stmt == StmtKind.ReturnK:
        if tree.child[0]:  # Si hay expresión de retorno
            # Verificación de tipos debería ir aquí
            pass

    # Procesar todos los hijos del nodo actual
    for i in range(MAXCHILDREN):
        _buildSymbolTable(tree.child[i], current_scope)
    
    # Procesar hermanos del nodo actual
    _buildSymbolTable(tree.sibling, current_scope)

    
def semantica(tree, imprime=True):
    print("\nIniciando análisis semántico...")
    tables = tabla(tree, imprime)
    
    if imprime:
        print("\nResumen:")
        print(f"Total de tablas de símbolos creadas: {len(tables)}")
        for i, table in enumerate(tables):
            print(f"Tabla #{i+1}: {len(table.symbols)} símbolos")
    
    return tables