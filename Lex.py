import ply.lex as lex
import sys
# KEYWORDS

tokens = [
    'PROGRAM', 'VARIABLES', 'FUNCTION', 'MAIN', 'RETURN', 'READ', 'WRITE',
    'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FROM', 'TO', 'SEMICOLON',
    'COMA', 'COLON', 'L_BRACE', 'R_BRACE', 'L_PAREN', 'R_PAREN', 'L_BRACKET',
    'R_BRACKET', 'EQUAL', 'PLUS', 'MINUS', 'MULT', 'DIV', 'AND', 'OR',
    'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL', 'DIFF', 'EQUALTO',
    'INTVAL', 'FLOATVAL', 'CHARVAL', 'STRING', 'INT', 'FLOAT', 'CHAR', 'VOID',
    'ID'
]
# REGEX
t_PROGRAM = r'Program'
t_VARIABLES = r'Var'
t_FUNCTION = r'Function'
t_MAIN = r'Main'
t_RETURN = r'Return'
t_READ = r'Read'
t_WRITE = r'Write'
t_IF = r'If'
t_THEN = r'Then'
t_ELSE = r'Else'
t_WHILE = r'While'
t_DO = r'Do'
t_FROM = r'From'
t_TO = r'To'
t_SEMICOLON = r'\;'
t_COMA = r'\,'
t_COLON = r'\:'
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_EQUAL = r'\='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_AND = r'\&'
t_OR = r'\|'
t_LESS = r'\<'
t_GREATER = r'\>'
t_LESSEQUAL = r'\<\='
t_GREATEREQUAL = r'\>\='
t_DIFF = r'\!\='
t_EQUALTO = r'\=\='
t_INTVAL = r'[-]?[0-9]+'
t_FLOATVAL = r'[-]?[0-9]+([.][0-9]+)'
t_CHARVAL = r'(\'[^\']\')'
t_STRING = r'\"[\w\d\s\,. ]*\"'
t_INT = r'Int'
t_FLOAT = r'Float'
t_CHAR = r'Char'
t_VOID = r'Void'

t_ID = r'([a-z][a-zA-Z0-9]*)'

# Tabs
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Lexer errors


def t_error(t):
    print(f"Invalid character '{t.value[0]}' on line '{t.lexer.lineno}'")
    t.lexer.skip(1)
    sys.exit()

# Comments


def t_comment(t):
    r'\#.*'
    pass


lexer = lex.lex()
