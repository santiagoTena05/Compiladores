# Proyecto de Compiladores - Lenguaje C-
Santiago Tena

Este repositorio contiene el desarrollo de un compilador básico para el lenguaje **C-**, realizado como parte del curso de **Compiladores**. El proyecto se implementa en Python e incluye las siguientes fases del proceso de compilación:

## 🔧 Componentes del proyecto

### 1. Analizador Léxico (Lexer)
El analizador léxico se encarga de leer el código fuente en C- y transformarlo en una secuencia de tokens. Utiliza una tabla de transiciones para reconocer:
- Palabras reservadas (`if`, `else`, `int`, `void`, `return`, `while`)
- Identificadores
- Números
- Símbolos especiales (`+`, `-`, `*`, `/`, `<=`, `<`, `>`, `>=`, `==`, `!=`, `=`, `;`, `,`, `(`, `)`, `{`, `}`, `[`, `]`)
- Comentarios de bloque (`/* ... */`)

### 2. Analizador Sintáctico (Parser)
El parser toma la secuencia de tokens generada por el lexer y construye el árbol sintáctico abstracto (AST). Se basa en una gramática LL(1) para el lenguaje C- y valida la estructura del código fuente, identificando errores de sintaxis.

### 3. Analizador Semántico
El analizador semántico recorre el AST para verificar reglas semánticas como:
- Declaración de variables y funciones antes de su uso
- Tipos compatibles en asignaciones y expresiones
- Reglas de ámbito y visibilidad
- Validación de la función `main`



