from Lex import tokens
import ply.yacc as yacc
import sys

# SEMANTIC CUBE

SEMANTIC_CUBE = {
    "INT" : {
        "+" : {
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "-" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False   
        },
        "*" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False 
        },
        "/" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "<" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        ">" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "!=" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "==" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        }
        

        
    },
    "FLOAT" : {
        "+" : {
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "-" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False   
        },
        "*" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False 
        },
        "/" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "<" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        ">" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "!=" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        },
        "==" :{
            "INT" :True,
            "FLOAT" :True,
            "STRING" :False
        }

    },
    "STRING" :{
         "+" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :True
         },
         "-" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :False
         },
        "*" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :False
         },
         "/" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :False
         },
        "<" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :False
         },
         ">" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :False
         },
        "!=" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :False
         },
         "==" :{
            "INT" :False,
            "FLOAT" :False,
            "STRING" :False
         }

    }

}



# GRAMMAR


def p_programa(p):
    '''programa : PROGRAM PARENTESIS_L PARENTESIS_R bloque'''


def p_bloque(p):
    '''bloque : CURLY_L var1 estatuto1 CURLY_R'''


def p_var1(p):
    '''var1 : var2
            | empty'''


def p_var2(p):
    '''var2 : VAR var3
            | var2 var2'''


def p_var3(p):
    '''var3 : var4 COLON tipo SEMICOLON'''


def p_var4(p):
    '''var4 : ID
              | var4 COMA var4'''


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING'''


def p_estatuto1(p):
    '''estatuto1 : estatuto2 SEMICOLON
                | estatuto1 estatuto1'''


def p_estatuto2(p):
    '''estatuto2 : asignacion 
                | condicion
                | llamado
                | whileLoop
                | forLoop'''


def p_asignacion(p):
    '''asignacion : ID ASSIGN expresion'''


def p_llamado(p):
    '''llamada_de_funciones : ID PARENTESIS_L llamado_1 PARENTESIS_R'''


def p_llamado_1(p):
    '''llamado_1 : llamado_2
                    | llamado_2 COMA llamado_2'''


def p_llamado_2(p):
    '''llamado_2 : STRING
                    | expresion'''


def p_expresion(p):
    '''expresion : exp
    | exp MORE exp
    | exp LESS exp
    | exp EQUAL exp
    | exp NOT_EQUAL exp'''


def p_whileLoop(p):
    '''whileLoop : WHILE PARENTESIS_L expresion PARENTESIS_R bloque'''


def p_forLoop(p):
    '''forLoop : FOR PARENTESIS_L argumento expresion SEMICOLON expresion PARENTESIS_R bloque'''


def p_condicion(p):
    '''condicion : IF PARENTESIS_L expresion PARENTESIS_R bloque condicion2'''


def p_condicion2(p):
    '''condicion2 : ELSE bloque
                     | empty'''


def p_argumento(p):
    '''argumento : argumento2
                  | empty'''


def p_argumento2(p):
    '''argumento2 : ID COLON tipo
            | argumento2 COMA argumento2'''


def p_exp(p):
    '''exp : termino
           | termino signo'''


def p_signo(p):
    '''signo : PLUS
             | MINUS'''


def p_termino(p):
    '''termino : factor
               | factor operacion'''


def p_operacion(p):
    '''operacion : MULT exp
                 | DIV exp'''


def p_factor(p):
    '''factor : PARENTESIS_L expresion PARENTESIS_R
               | var_cte'''


def p_var_cte(p):
    '''var_cte : ID 
              | CTE_INT
              | CTE_FLOAT'''


def p_empty(p):
    '''empty :'''


def p_error(p):
    print("ERROR type Syntax", p)


parser = yacc.yacc()

filename = input("file name: ")


try:
    f = open(filename, 'r')
    data = f.read()
    f.close()
    parser.parse(data)
except:
    print("ERROR File")
