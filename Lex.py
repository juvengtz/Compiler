import ply.lex as lex
# KEYWORDS
keywords = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'func': 'FUNC',
    'main': 'MAIN',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'while': 'WHILE',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
}
# TOKENS
tokens = [
    'ID', 'SEMICOLON', 'COMA', 'COLON',
    'BRACKET_L', 'BRACKET_R', 'EQUAL', 'NOT_EQUAL', 'ASSIGN',
    'PARENTESIS_L', 'PARENTESIS_R', 'CURLY_L', 'CURLY_R',
    'CTE_STRING', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MORE', 'LESS',
    'CTE_INT', 'CTE_FLOAT', 'NOTEQUAL'
] + list(keywords.values())
# REGEX
t_SEMICOLON = r'\;'
t_COMA = r'\,'
t_COLON = r'\:'
t_BRACKET_L = r'\['
t_BRACKET_R = r'\]'
t_CURLY_L = r'\{'
t_CURLY_R = r'\}'
t_ASSIGN = r'\='
t_EQUAL = r'\=\='
t_NOTEQUAL = r'\!\='
t_PARENTESIS_L = r'\('
t_PARENTESIS_R = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MORE = r'\>'
t_LESS = r'\<'
t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CTE_FLOAT(t):
    r'[0-9]*\.[0-9]+'
    t.value = float(t.value)
    return t


def t_CTE_STRING(t):
    r'\"(\\.|[^"\\])*\"'
    t.value = str(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
