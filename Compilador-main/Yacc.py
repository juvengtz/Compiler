import ply.yacc as yacc
import sys
from Lexer import tokens, lexer
from Cubo_Semantico import *
from Cuadruplo import *
import pickle
from pprint import pprint


def p_programa(p):
    '''PROGRAMA : PROGRAM create_dirfunc ID  SEMICOLON vars2 func2 principal'''


def p_vars(p):
    '''vars : VAR tipo  COLON id_list SEMICOLON'''
    
def p_vars2(p):
    '''vars2 : vars vars2
             | empty'''


def p_id_list(p):
    '''id_list : id_list COMMA ID addvar array
               | ID addvar array'''


def p_array(p):
    '''array : L_BRACKET CTE_I addDim R_BRACKET jumpAddr
                    | empty'''


def p_tipo(p):
    '''tipo : INT current_type
            | FLOAT current_type
            | BOOL current_type
            | CHAR current_type'''


def p_func(p):
    '''func : FUNCTION tipo_func ID addfunc L_PAREN params R_PAREN vars2 L_BRACE funcJump estatuto_rep R_BRACE endFunc'''

def p_func2(p):
    '''func2 : func func2
             | empty'''

def p_tipo_func(p):
    '''tipo_func : INT current_type
                 | FLOAT current_type
                 | CHAR current_type
                 | BOOL current_type
                 | VOID current_type'''


def p_params(p):
    '''params : tipo ID addvar updateParams params2
             | empty'''
    
def p_params2(p):
    '''params2 : COMMA tipo ID addvar updateParams params2
            | empty'''


def p_principal(p):
    '''principal : MAIN start funcChange L_PAREN R_PAREN bloque endProc'''

def p_bloque(p):
    '''bloque : L_BRACE estatuto_rep R_BRACE'''


def p_estatuto_rep(p):
    '''estatuto_rep : estatuto estatuto_rep 
                     | empty'''


def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura
                | llamada
                | retorno
                | lectura
                | repeticion'''
                #| repeticion2'''


def p_asignacion(p):
    '''asignacion : ID stack_operand_id EQUAL stack_operator expOr np_asignacion SEMICOLON
                    | var_dim EQUAL stack_operator expOr np_asignacion SEMICOLON'''


def p_llamada(p):
    '''llamada : ID llamadaEra L_PAREN fakebottom parm checkParamNum R_PAREN checkparentesis Gosub'''
    

#def p_func_especial(p):
#   '''func_especial : media
#                     | moda
#                     | varianza
#                     | reg
#                     | plotxy'''
    



def p_retorno(p):
    '''retorno : RETURN L_PAREN expOr np_return R_PAREN SEMICOLON'''


def p_lectura(p):
    '''lectura : READ L_PAREN ID np_read R_PAREN SEMICOLON'''


def p_escritura(p):
    '''escritura : WRITE L_PAREN escritura_rep R_PAREN SEMICOLON'''


def p_escritura_rep(p):
    '''escritura_rep : escritura_rep COMMA escritura_aux
                      | escritura_aux'''


def p_escritura_aux(p):
    '''escritura_aux : CTE_S printString
                         | expOr np_print'''


def p_condicion(p):
    '''condicion : IF L_PAREN expOr R_PAREN GotoF THEN bloque else_aux'''


def p_else_aux(p):
    '''else_aux : ELSE Goto bloque end_if
                   | end_if'''


def p_repeticion(p):
    '''repeticion : WHILE addJump L_PAREN expOr R_PAREN GotoF DO bloque end_while'''

#def p_repeticion2(p):
 #   ''' repeticion2 : FOR ID EQUAL expOr TO expOr DO bloque'''

def p_parm(p):
    '''parm : expOr checkParam parm2
            | empty'''

def p_parm2(p):
    '''parm2 : COMMA expOr checkParam parm2
            | empty'''

def p_expOr(p):
    '''expOr : expAnd checkAndOr OR stack_operator expOr
             | expAnd checkAndOr '''

def p_expAnd(p):
    '''expAnd : expresion checkAndOr AND stack_operator expAnd
             | expresion checkAndOr'''

def p_expresion(p):
    '''expresion : exp checkrelop relop'''


def p_relop(p):
    '''relop : GT stack_operator expresion
             | LT stack_operator expresion
             | EQ stack_operator expresion
             | LEQ stack_operator expresion
             | GEQ stack_operator expresion
             | empty'''


def p_exp(p):
    '''exp : termino checkexp masmenos '''


def p_masmenos(p):
    '''masmenos : PLUS stack_operator exp
                | MINUS stack_operator exp
                | empty'''

def p_termino(p):
    '''termino : factor checkterm multdiv'''


def p_multdiv(p):
    '''multdiv : MULT stack_operator termino
               | DIV stack_operator termino
               | empty'''


def p_factor(p):
    '''factor : L_PAREN fakebottom expOr R_PAREN checkparentesis
              | var_cte'''


def p_var_cte(p):
    '''var_cte : ID stack_operand_id
                | llamada
               | CTE_I stack_operand_int
               | CTE_F stack_operand_float
               | CTE_CHAR stack_operand_char
               | var_dim'''
    
def p_var_dim(p):
    '''var_dim : ID stack_operand_id L_BRACKET verDim fakebottom expOr cuadVer R_BRACKET checkparentesis verDimNum cuadVarDim  '''


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p is not None:
        print("Syntax error in line " + str(p.lineno) + " " + str(p.value))
        sys.exit()
    else:
        print("Syntax error: p is None")
    print("Parsing stack:")
    for s in parser.symstack:
        print(s)
    print("dirFunc")
    print(dirFunc)
    print("Quadruples")
    print(Quadruples)
    print("Constants")
    print(Constants)
    
# GLOBAL VARIABLES


Operands_Stack = []
Operators_Stack = []

JumpStack = []

Quadruples = []
Constants = {}


CurrentFunc = 'global'
CurrentType = 'void'
CurrentID = ''
ReturnT = 0
ParamCount = 0
ParamPointer = 0
tempCount = 0
CallFunc = ''
VarDimTable = []
dimVarAux = ''
dimCounter = 0

dirFunc = {}
Quadruples.append(['GOTO', None, None, None])

# Directions
global_int = 1000
global_float = 2000
global_char = 3000
global_bool = 4000
local_int = 5000
local_float = 6000
local_char = 7000
local_bool = 8000
const_int = 9000
const_float = 10000
const_char = 11000
const_bool = 12000
temp_int = 13000
temp_float = 14000
temp_char = 15000
temp_bool = 16000
stringMemory = 17000
pointerInt = 18000
pointerFloat = 19000

# Semantics

#Crea una nueva función en el directorio de funciones
def p_create_dirfunc(p):
    'create_dirfunc :'
    global CurrentFunc, CurrentType
    dirFunc[CurrentFunc] = {'type': CurrentType,
                                'vars': {}, 'parameters': [], 'Start_dir': 0, 'size': 0}

#Establece la variable global CurrentType con el valor de p[-1]
def p_current_type(p):
    'current_type :'
    global CurrentType
    CurrentType = p[-1]

#Esta función agrega una variable al diccionario de variables de la función actual
def p_addvar(p):
    'addvar :'
    global CurrentFunc, CurrentType, CurrentID
    CurrentID = p[-1]
    if CurrentID in dirFunc[CurrentFunc]['vars']:
        print('Variable already declared')
        sys.exit()
    else:
        if CurrentFunc == 'global':
            address = get_global_Mem(CurrentType)
        else:
            address = get_local_Mem(CurrentType)
        dirFunc[CurrentFunc]['vars'][CurrentID] = {'type': CurrentType, 'dir': address, 'dim': []}

#Añade una función al diccionario de funciones
def p_addfunc(p):
    'addfunc :'
    global CurrentFunc, CurrentType, CurrentID, ReturnT
    ReturnT = 0
    CurrentFunc = p[-1]
    if CurrentFunc in dirFunc:
        print('Function already declared')
        sys.exit()
    else:
        dirFunc[CurrentFunc] = {'type': CurrentType,
                              'vars': {}, 'parameters': [], 'Start_dir': 0, 'size': 0}
        address = get_global_Mem(CurrentType)
        dirFunc['global']['vars'][CurrentFunc] = {'type': CurrentType, 'dir': address, 'dim': []}


def get_global_Mem(type):
    global global_int, global_float, global_char, global_bool
    if type == 'int':
        if global_int < 2000:
            global_int += 1
            return global_int
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'float':
        if global_float < 3000:
            global_float += 1
            return global_float
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'char':
        if global_char < 4000:
            global_char += 1
            return global_char
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'bool':
        if global_bool < 5000:
            global_bool += 1
            return global_bool
        else:
            print('Stack overflow')
            sys.exit()


def get_local_Mem(type):
    global local_int, local_float, local_char, local_bool
    if type == 'int':
        if local_int < 6000:
            local_int += 1
            return local_int
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'float':
        if local_float < 7000:
            local_float += 1
            return local_float
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'char':
        if local_char < 8000:
            local_char += 1
            return local_char
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'bool':
        if local_bool < 9000:
            local_bool += 1
            return local_bool
        else:
            print('Stack overflow')
            sys.exit()

def get_const_Mem(type):
    global const_int, const_float, const_char, const_bool, stringMemory
    if type == 'int':
        if const_int < 10000:
            const_int += 1
            return const_int
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'float':
        if const_float < 11000:
            const_float += 1
            return const_float
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'char':
        if const_char < 12000:
            const_char += 1
            return const_char
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'bool':
        if const_bool < 13000:
            const_bool += 1
            return const_bool
    elif type == 'string':
        if stringMemory < 18000:
            stringMemory += 1
            return stringMemory
        else:
            print('Stack overflow')
            sys.exit()

def get_temp_Mem(type):
    global temp_int, temp_float, temp_char, temp_bool
    if type == 'int':
        if temp_int < 14000:
            temp_int += 1
            return temp_int
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'float':
        if temp_float < 15000:
            temp_float += 1
            return temp_float
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'char':
        if temp_char < 16000:
            temp_char += 1
            return temp_char
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'bool':
        if temp_bool < 17000:
            temp_bool += 1
            return temp_bool
        else:
            print('Stack overflow')
            sys.exit()

def get_nextAddrVarDim(type,size):
    global global_int, global_float, global_char, global_bool, local_int, local_float, local_char, local_bool
    if type == 'int':
        if global_int < 2000:
            global_int += size
            
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'float':
        if global_float < 3000:
            global_float += size
            
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'char':
        if global_char < 4000:
            global_char += size
            
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'bool':
        if global_bool < 5000:
            global_bool += size
        
        else:
            print('Stack overflow')
            sys.exit()


def getPointerVar(type):
    global pointerInt, pointerFloat
    if type == 'int':
        if pointerInt < 19000:
            pointerInt += 1
            return pointerInt
        else:
            print('Stack overflow')
            sys.exit()
    elif type == 'float':
        if pointerFloat < 20000:
            pointerFloat += 1
            return pointerFloat
        else:
            print('Stack overflow')
            sys.exit()

def reset_local_Mem():
    global local_int, local_float, local_char, local_bool
    local_int = 5000
    local_float = 6000
    local_char = 7000
    local_bool = 8000

# maneja la operación de apilar un operando identificador en la pila de operandos
def p_stack_operand_id(p):
    'stack_operand_id :'
    global Operands_Stack, Operators_Stack, dirFunc, CurrentFunc

    var_name = p[-1]
    if var_name in dirFunc[CurrentFunc]['vars']:
        var_info = dirFunc[CurrentFunc]['vars'][var_name]
    elif var_name in dirFunc['global']['vars']:
        var_info = dirFunc['global']['vars'][var_name]
    else:
        print('Variable not declared: ' + var_name + ' in ' + CurrentFunc)
        sys.exit()

    var_type = var_info.get('type')
    var_address = var_info.get('dir')

    Operands_Stack.append({'name': var_name, 'type': var_type, 'dir': var_address})


#Apila un operando entero en la pila de operandos
def p_stack_operand_int(p):
    'stack_operand_int :'
    global Operands_Stack, Constants
    idName = p[-1]
    
    if p[-1] not in Constants:
        address = get_const_Mem('int')
        Constants[idName] = {'dir': address, 'type': 'int'}
    else:
        address = Constants[idName].get('dir')
    Operands_Stack.append({'name': idName, 'type': 'int', 'dir': address})


#Apila un operando flotante en la pila de operandos
def p_stack_operand_float(p):
    'stack_operand_float :'
    global Operands_Stack, Constants
    idName = p[-1]
    
    if p[-1] not in Constants:
        address = get_const_Mem('float')
        Constants[idName] = {'dir': address, 'type': 'float'}
    else:
        address = Constants[idName].get('dir')
    Operands_Stack.append({'name': idName, 'type': 'float', 'dir': address})

#Apila un operando caracter en la pila de operandos
def p_stack_operand_char(p):
    'stack_operand_char :'
    global Operands_Stack, Constants
    idName = p[-1]
    
    if p[-1] not in Constants:
        address = get_const_Mem('char')
        Constants[idName] = {'dir': address, 'type': 'char'}
    else:
        address = Constants[idName].get('dir')
    Operands_Stack.append({'name': idName, 'type': 'char', 'dir': address})

#Añade el operador a la pila de operadores
def p_stack_operator(p):
    'stack_operator :'
    global Operators_Stack
    Operators_Stack.append(p[-1])

#agrega un paréntesis abierto "(" a la pila de operadores
def p_fakebottom(p):
    'fakebottom :'
    global Operators_Stack
    Operators_Stack.append('(')
#Verifica si hay un paréntesis en la pila de operadores. Si hay un paréntesis de apertura, lo elimina de la pila.
def p_checkparentesis(p):
    'checkparentesis :'
    global Operators_Stack
    if Operators_Stack[-1] == '(':
        Operators_Stack.pop()
    else:
        print('Parentesis mismatch')
        sys.exit()

# agrega los cuádruplos AND OR a la lista de cuádruplos
def p_checkAndOr(p):
    'checkAndOr :'
    global Operators_Stack, Quadruples,tempCount
    if Operators_Stack:
        if Operators_Stack[-1] == '&' or Operators_Stack[-1] == '|':
            right_operand = Operands_Stack.pop()
            left_operand = Operands_Stack.pop()
            operator = Operators_Stack.pop()
            cubo_semantico = CuboSemantico()  
            result_type = cubo_semantico.get_type(left_operand['type'], right_operand['type'], operator)
            if result_type != 'error':
                address = get_temp_Mem(result_type)
                Operands_Stack.append({'name': 'temp', 'type': result_type, 'dir': address})
                Quadruples.append([operator, left_operand['dir'],
                                right_operand['dir'], address])
                tempCount += 1
            else:
                print('Type mismatch 1')
                sys.exit()

# agrega los cuádruplos * / a la lista de cuádruplos
def p_checkterm(p):
    'checkterm :'
    global Operators_Stack, Quadruples,tempCount
    if Operators_Stack:
        if Operators_Stack[-1] == '*' or Operators_Stack[-1] == '/':
            right_operand = Operands_Stack.pop()
            left_operand = Operands_Stack.pop()
            operator = Operators_Stack.pop()
            cubo_semantico = CuboSemantico()  
            result_type = cubo_semantico.get_type(left_operand['type'], right_operand['type'], operator)
            if result_type != 'error':
                address = get_temp_Mem(result_type)
                Operands_Stack.append({'name': 'temp', 'type': result_type, 'dir': address})
                Quadruples.append([operator, left_operand['dir'],
                                right_operand['dir'], address])
                tempCount += 1
            else:
                print('Type mismatch 2')
                sys.exit()
        
# agrega los cuádruplos + - a la lista de cuádruplos
def p_checkexp(p):
    'checkexp :'
    global Operators_Stack, Quadruples,tempCount
    if Operators_Stack: 
        if Operators_Stack[-1] == '+' or Operators_Stack[-1] == '-':
            right_operand = Operands_Stack.pop()
            left_operand = Operands_Stack.pop()
            operator = Operators_Stack.pop()
            cubo_semantico = CuboSemantico()  
            result_type = cubo_semantico.get_type(left_operand['type'], right_operand['type'], operator)
            if result_type != 'error':
                address = get_temp_Mem(result_type)
                Operands_Stack.append({'name': 'temp', 'type': result_type, 'dir': address})
                Quadruples.append([operator, left_operand['dir'],
                                right_operand['dir'], address])
                tempCount += 1
            else:
                print('Type mismatch 3')
                sys.exit()

# agrega los cuádruplos comparadores a la lista de cuádruplos
def p_checkrelop(p):
    'checkrelop :'
    global Operators_Stack, Quadruples,tempCount
    if Operators_Stack:
        if Operators_Stack[-1] == '<' or Operators_Stack[-1] == '>' or Operators_Stack[-1] == '<=' or Operators_Stack[-1] == '>=' or Operators_Stack[-1] == '==':
            right_operand = Operands_Stack.pop()
            left_operand = Operands_Stack.pop()
            operator = Operators_Stack.pop()
            cubo_semantico = CuboSemantico()
            result_type = cubo_semantico.get_type(left_operand['type'], right_operand['type'], operator)
            if result_type != 'error':
                address = get_temp_Mem(result_type)
                Operands_Stack.append({'name': 'temp', 'type': result_type, 'dir': address})
                Quadruples.append([operator, left_operand['dir'],
                                right_operand['dir'], address])
                tempCount += 1
            else:
                print('Type mismatch 4')
                sys.exit()

# agrega el cuádruplo ERA a la lista de cuádruplos
def p_llamdaEra(p):
    'llamadaEra :'
    global Operands_Stack, Operators_Stack, Quadruples, CurrentFunc, dirFunc, CallFunc
    CallFunc = p[-1]
    if p[-1] in dirFunc:
        Quadruples.append(['ERA', None, None, CallFunc])
    else:
        print('Function not declared')
        sys.exit()


# agrega el cuádruplo de asignacion a la lista de cuádruplos
def p_np_asignacion(p):
    'np_asignacion :'
    global Operands_Stack, Operators_Stack, Quadruples, CurrentFunc, dirFunc
    if Operators_Stack[-1] == '=':
        operando = Operands_Stack.pop()
        right_operand = operando['dir']
        right_type = operando['type']
        idOperand = Operands_Stack.pop()
        left_operand = idOperand['dir']
        left_type = idOperand['type']
        operator = Operators_Stack.pop()
        cubo_semantico = CuboSemantico()  
        result_type = cubo_semantico.get_type(left_type, right_type, operator)
        
        if result_type != 'error':
            Quadruples.append([operator, right_operand, None, left_operand])
        else:
            print('Type mismatch 5')
            sys.exit()

# agrega el cuádruplo Return a la lista de cuádruplos
def p_np_return(p):
    'np_return :'
    global Operands_Stack, Operators_Stack, Quadruples, CurrentFunc, dirFunc, ReturnT
    right_operand = Operands_Stack.pop()
    result_type = dirFunc[CurrentFunc]['type']
    if right_operand['type'] == result_type:
        ReturnT = 1
        Quadruples.append(['return', None, None, right_operand['dir']])
    else:
        print('Type mismatch 6')
        sys.exit()

# agrega el cuádruplo GOTOF a la lista de cuádruplos
def p_GotoF(p):
    'GotoF :'
    global Operands_Stack, Operators_Stack, Quadruples, JumpStack
    result = Operands_Stack.pop()
    if result['type'] == 'bool':
        Quadruples.append(['GOTOF', result['dir'], None, None])
        JumpStack.append(len(Quadruples) - 1)
    else:
        print('Type mismatch 7')
        sys.exit()

# agrega el cuádruplo GOTO a la lista de cuádruplos
def p_Goto(p):
    'Goto :'
    global Operands_Stack, Operators_Stack, Quadruples, JumpStack
    Quadruples.append(['GOTO', None, None, None])
    false = JumpStack.pop()
    JumpStack.append(len(Quadruples) - 1)
    Quadruples[false][3] = len(Quadruples)

#Finaliza una instrucción "if" en el analizador sintáctico
def p_end_if(p):
    'end_if :'
    global Operands_Stack, Operators_Stack, Quadruples, JumpStack
    end = JumpStack.pop()
    Quadruples[end][3] = len(Quadruples)

#Desapila los elementos necesarios de las pilas y genera el cuádruplo GOTO para finalizar un bucle while
def p_end_while(p):
    'end_while :'
    global Operands_Stack, Operators_Stack, Quadruples, JumpStack
    end = JumpStack.pop()
    ret = JumpStack.pop()
    Quadruples.append(['GOTO', None, None, ret])
    Quadruples[end][3] = len(Quadruples)

#Añade un salto a la pila de saltos
def p_addJump(p):
    'addJump :'
    global Operands_Stack, Operators_Stack, Quadruples, JumpStack
    JumpStack.append(len(Quadruples))

#Agrega el cuádruplo 'ENDFUNC' a la lista de cuádruplos
def p_endFunc(p):
    'endFunc :'
    global Operands_Stack, Operators_Stack, Quadruples, JumpStack, ReturnT, CurrentFunc, dirFunc,tempCount
    result_type = dirFunc[CurrentFunc]['type']
    dirFunc[CurrentFunc]['size'] += tempCount
    if result_type != 'void' and ReturnT == 0:
        print('Function has to return a value')
        sys.exit()
    
    if result_type == 'void' and ReturnT == 1:
        print('Function should not have a return')
        sys.exit()
    tempCount = 0
    Quadruples.append(['ENDFUNC', None, None, None])
    reset_local_Mem()
    ReturnT = 0

#Actualiza los parámetros de la función actual
def p_updateParams(p):
    'updateParams :'
    global dirFunc, CurrentFunc, CurrentType, CurrentID, ParamCount
    var = dirFunc[CurrentFunc]['vars'][CurrentID]
    address = var.get('dir')
    tipo = var.get('type')
    dirFunc[CurrentFunc]['parameters'].append([tipo, address])
    ParamCount += 1

#Establece la dirección de inicio de una función en el diccionario dirFunc,actualiza el tamaño de la función
def p_funcJump(p):
    'funcJump :'
    global dirFunc,Quadruples, CurrentFunc, ParamCount
    dirFunc[CurrentFunc]['Start_dir'] = len(Quadruples)
    dirFunc[CurrentFunc]['size'] += ParamCount
    ParamCount = 0

#Cambia la función actual a "global"
def p_funcChange(p):
    'funcChange :'
    global CurrentFunc
    CurrentFunc = 'global'

## agrega el cuádruplo PRINT a la lista de cuádruplos
def p_np_print(p):
    'np_print :'
    global Operands_Stack, Quadruples
    result = Operands_Stack.pop()
    Quadruples.append(['PRINT',None,None,result['dir']])
#Imprime una String, agrega el cuádruplo PRINT a la lista de cuádruplos
def p_printString(p):
    'printString :'
    global Operands_Stack, Quadruples
    address = get_const_Mem('string')
    Constants[p[-1]] = {'dir': address, 'type': 'string'}
    Quadruples.append(['PRINT',None,None,address])

# agrega el cuádruplo READ a la lista de cuádruplos
def p_np_read(p):
    'np_read :'
    global dirFunc, CurrentFunc, Quadruples
    variable_name = p[-1]
    if variable_name not in dirFunc[CurrentFunc]['vars']:
        print('Variable not declared')
        sys.exit()
    else:
        address = dirFunc[CurrentFunc]['vars'][variable_name].get('dir')
        Quadruples.append(['READ', None, None, address])

#Inicia el analisis sintáctico
def p_start(p):
    'start :'
    global Quadruples
    Quadruples[0][3] = len(Quadruples)

# agrega el cuádruplo ENDPROC a la lista de cuádruplos
def p_endProc(p):
    'endProc :'
    global Operands_Stack, Operators_Stack, Quadruples, JumpStack
    Quadruples.append(['ENDPROC', None, None, None])

#comprobar si el tipo del parámetro pasado coincide con el tipo esperado, si si, agrega el cuádruplo PARAM a la lista de cuádruplos
def p_checkParam(p):
    'checkParam :'
    global Operands_Stack, Quadruples, CallFunc, ParamPointer, dirFunc

    arg = Operands_Stack.pop()
    argType = arg.get('type')
    paramType = dirFunc[CallFunc]['parameters'][ParamPointer][0]
    

    if argType == paramType:
        paramAddr = dirFunc[CallFunc]['parameters'][ParamPointer][1]
        argAddr = arg.get('dir')
        Quadruples.append(['PARAM', None, argAddr, paramAddr])
        ParamPointer += 1
    else:
        print('Parameter types do not match')

#Verifica si el número de parámetros coincide
def p_checkParamNum(p):
    'checkParamNum :'
    global Operands_Stack, Quadruples, CallFunc, ParamPointer, dirFunc
    if (ParamPointer != len(dirFunc[CallFunc]['parameters'])):
        print('Number of parameters does not match')
        sys.exit()


# agrega el cuádruplo GOSUB a la lista de cuádruplos y agrega el cuádruplo de asignación a la lista de cuádruplos
def p_Gosub(p):
    'Gosub :'
    global Operands_Stack, Quadruples, CallFunc, ParamPointer, dirFunc

    Quadruples.append(['GOSUB', None, None, CallFunc])

    tipo = dirFunc['global']['vars'][CallFunc].get('type')
    if tipo != 'void':
        dirResult = dirFunc['global']['vars'][CallFunc].get('dir')
        nextDir = get_temp_Mem(tipo)
        Quadruples.append(['=', dirResult, None, nextDir])
        Operands_Stack.append({'name': 'temp', 'type': tipo, 'dir': nextDir})

    ParamPointer = 0



#Añade una dimensión a una variable en la pila de operandos
def p_addDim(p):
    'addDim :'
    global Operands_Stack, Quadruples, dirFunc, CurrentFunc, Constants
    if(p[-1] <= 0):
        print('Dimension must be greater than 0')
        sys.exit()
    else:
        addr = get_const_Mem('int')
        dirFunc[CurrentFunc]['vars'][CurrentID]['dim'].append([p[-1]])
        if(p[-1] not in Constants):
            Constants[p[-1]] = {'dir': addr, 'type': 'int'}

#Salto a dirección de salto
def p_jumpAddr(p):
    'jumpAddr :'
    global dirFunc, CurrentFunc, Quadruples,CurrentID, CurrentType
    if(CurrentType == 'int' or CurrentType == 'float'):
       val1 = dirFunc[CurrentFunc]['vars'][CurrentID]['dim'][0][0]
       get_nextAddrVarDim(CurrentType,val1-1)
    else:
        print('Type mismatch')
        sys.exit()

#Verifica si la variable tiene la dimensión adecuada
def p_verDim(p):
    'verDim :'
    global dirFunc, CurrentFunc, Quadruples,CurrentID, CurrentType, dimCounter, dimVarAux
    if dimCounter == 0:
        top = Operands_Stack.pop()
        dimVarAux = top.get('name')     
    if dirFunc[CurrentFunc]['vars'][dimVarAux]['dim'] [dimCounter] == None:
        print("variable does not have the size", dimVarAux)
        sys.exit()
    dimCounter += 1


#Verifica si el número de dimensiones coincide con la variable
def p_verDimNum(p):
    'verDimNum :'
    global dirFunc, dimCounter, dimCounter, CurrentFunc, dimVarAux
    if (len(dirFunc[CurrentFunc]['vars'][dimVarAux]['dim']) !=  dimCounter):
        print("number of dimensions mismatch the variable") 
        sys.exit()
        
#Verifica si el valor en la cima de la pila de operandos está dentro de los límites establecidos
def p_cuadVer(p):
    'cuadVer :'
    global Operands_Stack, Quadruples, Constants, dimCounter, dimVarAux, dirFunc, CallFunc
    top = Operands_Stack[-1].get('dir')
    val = dirFunc[CurrentFunc]['vars'][dimVarAux]['dim'][dimCounter-1][0]
    valAddr = Constants[val].get('dir')
    Quadruples.append(['VER', None, top, valAddr])

#Función que maneja la generación de cuádruplos para variables dimensionadas   
def p_cuadVarDim(p):
    'cuadVarDim :'
    global dimCounter, Operands_Stack, CurrentFunc, dirFunc, Constants, dimVarAux
    dirBase = dirFunc[CurrentFunc]['vars'][dimVarAux].get('dir')
    tipo = dirFunc[CurrentFunc]['vars'][dimVarAux].get('type')
    if(dirBase not in Constants):
        address = get_const_Mem('int')
        Constants[dirBase] = {'dir': address,'type': 'int'}

        address = Constants[dirBase].get('dir')
        dim1 = Operands_Stack.pop()
        addrPtr = getPointerVar(tipo)
        print('tipo',tipo)
        print("addrPtr",addrPtr)
        print(dimVarAux)
        Quadruples.append(['+',dim1.get('dir'),address,addrPtr])
        Operands_Stack.append({'name':'indexVal','type':'int','dir': addrPtr})
        dimCounter = 0


parser = yacc.yacc()


if __name__ == "__main__":
   # data = input('file name:')
    with open("./search.txt", 'r') as data:
        parser.parse(data.read())
        
    pprint(dirFunc)
    for i, quad in enumerate(Quadruples):
        print(f"Quad {i}: {quad}")
    pprint(Constants)

    with open('dirFunc.pkl', 'wb') as f:
        pickle.dump(dirFunc, f)

    with open('Constants.pkl', 'wb') as f:
        pickle.dump(Constants, f)

    with open('Quadruples.pkl', 'wb') as f:
        pickle.dump(Quadruples, f)