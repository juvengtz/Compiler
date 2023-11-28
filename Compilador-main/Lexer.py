import ply.lex as lex

tokens = [
    'ID', 'CTE_I', 'CTE_F', 'CTE_S', 'CTE_CHAR',
    'PLUS', 'MINUS', 'MULT', 'DIV', 'EQUAL',
    'GT', 'LT', 'EQ', 'LEQ', 'GEQ', 'COLON',
    'SEMICOLON', 'COMMA', 'L_PAREN', 'R_PAREN',
    'L_BRACKET', 'R_BRACKET', 'L_BRACE', 'R_BRACE',
    'AND', 'OR'
]

reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'bool': 'BOOL',
    'void' : 'VOID',
    'main': 'MAIN',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'read': 'READ',
    'write': 'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'to': 'TO',
    'do': 'DO',
    'media': 'MEDIA',
    'moda': 'MODA',
    'Varianza': 'VARIANZA',
    'Reg': 'REG',
    'PlotXY': 'PLOTXY'
}

tokens += list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_EQUAL = r'='
t_GT = r'>'
t_LT = r'<'
t_EQ = r'=='
t_LEQ = r'<='
t_GEQ = r'>='
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_AND = r'\&'
t_OR = r'\|'
t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_CTE_F(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CTE_I(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CTE_S(t):
    r'\".*?\"'
    t.value = str(t.value)
    return t


def t_CTE_CHAR(t):
    r'\'.?\''
    t.value = str(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)


lexer = lex.lex()
