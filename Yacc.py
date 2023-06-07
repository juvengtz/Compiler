import ply.lex as lex
import ply.yacc as yacc
import sys
from collections import deque

from Semantic_cube import *
from Quadruple import *
# GRAMMAR


c = 0
prog_name = ''
curr_func_name = ''
curr_func_type = ''
curr_currVarName = ''
curr_var_type = ''
curr_for_assign = 0
param_counter = 0
param_receive_counter = 0
exists_return = 0
call_origin = 0
function_params = {}
var_size = 1
for_var_stack = deque()
vars_stack = deque()
operators_stack = deque()
terms_stack = deque()
types_stack = deque()
variables_table = {}
constants_table = {'Int': {}, 'Float': {}, 'Char': {}, 'String': {}}
quadruples = []
jumps_stack = []

# Memoria
global_mem_int = 1000
global_mem_float = 2000
global_mem_char = 3000
local_mem_int = 4000
local_mem_float = 5000
local_mem_char = 6000
constant_mem_int = 7000
constant_mem_float = 8000
constant_mem_char = 9000
mem_strings = 10000

# LEXER


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

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Invalid character '{t.value[0]}' on line '{t.lexer.lineno}'")
    t.lexer.skip(1)
    sys.exit()

# Comments


def t_comment(t):
    r'\#.*'
    pass


lexer = lex.lex()

# Sintax


def p_program(p):
    '''
    program : PROGRAM ID np_program SEMICOLON variables functions MAIN np_main L_PAREN R_PAREN block np_endProgram empty
    '''
    p[0] = None


def p_variables(p):
    '''
    variables : VARIABLES variablesU
              | empty

    variablesU : variablesD
               | empty

    variablesD : ID np_addVariableToStack COMA variablesD
               | ID COLON var_type np_addVariable SEMICOLON variablesU
               | ID L_BRACKET INTVAL R_BRACKET COLON var_type np_addArray SEMICOLON variablesU
    '''
    p[0] = None


def p_functions(p):
    '''
    functions : functionsU
              | empty

    functionsU : func_type FUNCTION ID np_addFunction L_PAREN receive_params R_PAREN variables block np_endFunction functionsD

    functionsD : functions
               | empty
    '''
    p[0] = None


def p_func_type(p):
    '''
    func_type : INT empty
              | FLOAT empty
              | CHAR empty
              | VOID empty
    '''
    p[0] = p[1]


def p_var_type(p):
    '''
    var_type : INT empty
             | FLOAT empty
             | CHAR empty
    '''
    p[0] = p[1]


def p_receive_params(p):
    '''
    receive_params : ID COLON var_type np_receiveParams receive_paramsD empty
                   | empty

    receive_paramsD : COMA receive_params empty
                    | empty
    '''
    p[0] = None


def p_send_params(p):
    '''
    send_params : hyper_exp np_sentParam send_paramsD empty
                | empty

    send_paramsD : COMA send_params empty
                 | empty
    '''
    p[0] = None


def p_block(p):
    '''
    block : L_BRACE blockU R_BRACE empty

    blockU : statement blockD np_emptyStacks empty
           | empty

    blockD : blockU empty
           | empty
    '''
    p[0] = None


def p_statement(p):
    '''
    statement : assignment SEMICOLON empty
              | call np_isStatement SEMICOLON empty
              | return SEMICOLON empty
              | read SEMICOLON empty
              | write SEMICOLON empty
              | decision empty
              | conditional empty
              | non_conditional empty
              | empty
    '''


def p_assignment(p):
    '''
    assignment : ID np_addID EQUAL np_addOperator hyper_exp np_assignment empty
               | ID L_BRACKET np_fakeBottom hyper_exp R_BRACKET np_addArrayID EQUAL np_addOperator hyper_exp np_assignment empty
    '''
    p[0] = None


def p_call(p):
    '''
    call : ID np_call_era L_PAREN send_params np_paramValidation R_PAREN np_call_gosub empty
    '''
    p[0] = None


def p_return(p):
    '''
    return : RETURN L_PAREN hyper_exp np_return R_PAREN empty
    '''
    p[0] = None


def p_read(p):
    '''
    read : READ L_PAREN ID np_read R_PAREN empty
    '''
    p[0] = None


def p_write(p):
    '''
    write : WRITE L_PAREN writeD R_PAREN empty

    writeD : hyper_exp np_write empty
           | STRING np_string empty
    '''
    p[0] = None


def p_decision(p):
    '''
    decision : IF L_PAREN hyper_exp R_PAREN np_startDecision THEN block decisionU np_endDecision empty

    decisionU : ELSE np_startDecisionElse block empty
              | empty
    '''
    p[0] = None


def p_conditional(p):
    '''
    conditional : WHILE L_PAREN np_conditionalBefore hyper_exp np_conditionalDuring R_PAREN DO block np_conditionalAfter empty
    '''
    p[0] = None


def p_non_conditional(p):
    '''
    non_conditional : FROM L_PAREN for_assignment R_PAREN TO hyper_exp np_boolFor DO block np_endCondition empty
    '''


def p_for_assignment(p):
    '''
    for_assignment : ID np_addIDFor EQUAL np_addOperator hyper_exp np_for_assignment empty
    '''
    p[0] = None


def p_operatorA(p):
    '''
    operatorA : PLUS np_addOperator empty
              | MINUS np_addOperator empty
    '''
    p[0] = None


def p_operatorT(p):
    '''
    operatorT : MULT np_addOperator empty
              | DIV np_addOperator empty
    '''
    p[0] = None


def p_operatorL(p):
    '''
    operatorL : OR np_addOperator empty
              | AND np_addOperator empty
    '''
    p[0] = None


def p_operatorR(p):
    '''
    operatorR : LESS np_addOperator empty
              | GREATER np_addOperator empty
              | LESSEQUAL np_addOperator empty
              | GREATEREQUAL np_addOperator empty
              | EQUALTO np_addOperator empty
              | DIFF np_addOperator empty
    '''
    p[0] = None


def p_hyper_exp(p):
    '''
    hyper_exp : super_exp np_doHyperExp hyper_expU

    hyper_expU : operatorL hyper_exp empty 
               | empty
    '''


def p_super_exp(p):
    '''
    super_exp : exp np_doSuperExp super_expU

    super_expU : operatorR super_exp empty 
               | empty
    '''


def p_exp(p):
    '''
    exp : term np_doExp expU

    expU : operatorA exp
         | empty
    '''


def p_term(p):
    '''
    term : factor np_doTerm termU

    termU : operatorT term 
          | empty
    '''


def p_factor(p):
    '''
    factor : varcte empty
           | call np_isExpression empty
           | L_PAREN hyper_exp R_PAREN empty
    '''
    p[0] = None


def p_varcte(p):
    '''
    varcte  : ID np_addID empty
            | ID L_BRACKET np_fakeBottom hyper_exp R_BRACKET np_addArrayID empty
            | INTVAL np_addConstInt empty
            | FLOATVAL np_addConstFloat empty
            | CHARVAL np_addConstChar empty
    '''
    p[0] = None


def p_error(p):
    print("Syntax error at line " + str(lexer.lineno))
    sys.exit()


def p_empty(p):
    '''
    empty : 
    '''


def p_np_program(p):
    'np_program : '
    global prog_name, curr_func_name
    prog_name = p[-1]
    curr_func_name = p[-1]
    variables_table[prog_name] = {'type': prog_name, 'variables': {}}
    quadruples.append(Quadruple('GOTO', None, None, prog_name))

# End the program


def p_np_endProgram(p):
    'np_endProgram : '
    quadruples.append(Quadruple('END', None, None, None))

# When starting a function


def p_np_addFunction(p):
    'np_addFunction : '
    global curr_func_name, curr_func_type, prog_name, memoryIntegerL, memoryFloatL, memoryCharL, returnExists
    returnExists = 0
    curr_func_name = p[-1]
    curr_func_type = p[-3]
    if curr_func_name not in variables_table.keys():
        variables_table[curr_func_name] = {'type': curr_func_type, 'quadrupleNum': len(
            quadruples), 'variables': {}, 'parameters': {}}
        if curr_func_type != 'Void':
            memory = p_get_global_memory(curr_func_type)
            variables_table[prog_name]['variables'][curr_func_name] = {
                'type': curr_func_type, 'memory': memory}

        # Reset local memory for functions
        memoryIntegerL = 4000
        memoryFloatL = 5000
        memoryCharL = 6000
    else:
        p_notifError(str(lexer.lineno) + " - The function " +
                     curr_func_name + " has already been declared")

# - When finishing a function


def p_np_endFunction(p):
    'np_endFunction : '
    global returnExists, curr_func_name
    if curr_func_type != 'Void' and returnExists == 0:
        p_notifError(str(lexer.lineno) + " - The function " +
                     curr_func_name + " does not have a return statement")
    elif curr_func_type == 'Void' and returnExists == 1:
        p_notifError(str(lexer.lineno) + " - The function " +
                     curr_func_name + " should not have return statements")
    else:
        quadruples.append(Quadruple('ENDFUNC', None, None, None))
        returnExists = 0


def p_np_main(p):
    'np_main : '
    global prog_name, curr_func_name
    curr_func_name = prog_name
    quadruples[0].result = len(quadruples)


# ADD VARIABLES
# Neural Point - Add variables to the variable table


def p_np_addVariable(p):
    'np_addVariable : '
    global curr_func_name, current_variable_name, current_variable_type, prog_name, variable_size
    current_variable_type = p[-1]
    current_variable_name = p[-3]
    variable_size = 1

    while vars_stack:
        if vars_stack[0] not in variables_table[curr_func_name]['variables'].keys() and vars_stack[0] not in variables_table[prog_name]['variables'].keys():
            memory = get_memory_for_ID(current_variable_type)
            variables_table[curr_func_name]['variables'][vars_stack[0]] = {
                'type': current_variable_type, 'memory': memory}
            vars_stack.popleft()
        else:
            p_notifError(str(lexer.lineno) + " - La variable " +
                         vars_stack[0] + " ya se declaró anteriormente")

    if (current_variable_name not in variables_table[curr_func_name]['variables'].keys()
            and current_variable_name not in variables_table[prog_name]['variables'].keys()):
        memory = get_memory_for_ID(current_variable_type)
        variables_table[curr_func_name]['variables'][current_variable_name] = {
            'type': current_variable_type, 'memory': memory}
    else:
        p_notifError(str(lexer.lineno) + " - The variable " +
                     current_variable_name + " has already been declared")


def p_np_addVariableToStack(p):
    'np_addVariableToStack :'
    global vars_stack
    current_variable_name = p[-1]
    vars_stack.append(current_variable_name)


def p_np_addArray(p):
    'np_addArray : '
    global curr_func_name, current_variable_name, current_variable_type, prog_name, variable_size
    current_variable_type = p[-1]
    current_variable_name = p[-6]
    variable_size = p[-4]

    if (current_variable_name not in variables_table[curr_func_name]['variables'].keys()
            and current_variable_name not in variables_table[prog_name]['variables'].keys()):
        memory = get_memory_for_ID(current_variable_type)
        variables_table[curr_func_name]['variables'][current_variable_name] = {
            'type': current_variable_type, 'memory': memory, 'size': variable_size}
        variable_size = 1
    else:
        p_notifError(str(lexer.lineno) + " - The array " +
                     current_variable_name + " has already been declared")


def p_np_addID(p):
    'np_addID : '
    global curr_func_name
    if p[-1] in variables_table[curr_func_name]['variables'].keys():
        terms_stack.append(
            variables_table[curr_func_name]['variables'][p[-1]]['memory'])
        types_stack.append(
            variables_table[curr_func_name]['variables'][p[-1]]['type'])

    elif p[-1] in variables_table[prog_name]['variables'].keys():
        terms_stack.append(
            variables_table[prog_name]['variables'][p[-1]]['memory'])
        types_stack.append(
            variables_table[prog_name]['variables'][p[-1]]['type'])
    else:
        p_notifError(str(lexer.lineno) +
                     " - No se declaró la variable " + p[-1])


def p_np_fakeBottom(p):
    'np_fakeBottom : '
    operators_stack.append('(')


def p_np_addArrayID(p):
    'np_addArrayID : '
    global curr_func_name, operators_stack
    operators_stack.pop()
    id = p[-5]
    dimension = terms_stack.pop()

    if variables_table[prog_name]['variables'][id]:
        quadruples.append(Quadruple('VERIFY', dimension, 0,
                          variables_table[prog_name]['variables'][id]['size']))
    elif variables_table[curr_func_name]['variables'][id]:
        quadruples.append(Quadruple(
            'VERIFY', dimension, 0, variables_table[curr_func_name]['variables'][id]['size']))
    else:
        p_notifError(str(lexer.lineno) + " - Variable " + id + " not declared")

    temp_memory = get_memory_for_ID('Int')

    if id in variables_table[curr_func_name]['variables'].keys():
        quadruples.append(Quadruple(
            'SUM_BASE', variables_table[curr_func_name]['variables'][id]['memory'], dimension, temp_memory))

        terms_stack.append("(" + str(temp_memory) + ")")
        types_stack.append(
            variables_table[curr_func_name]['variables'][id]['type'])
    elif id in variables_table[prog_name]['variables'].keys():
        quadruples.append(Quadruple(
            'SUM_BASE', variables_table[prog_name]['variables'][id]['memory'], dimension, temp_memory))

        terms_stack.append("(" + str(temp_memory) + ")")
        types_stack.append(
            variables_table[prog_name]['variables'][id]['type'])
    else:
        p_notifError(str(lexer.lineno) + " - Variable " + id + " not declared")


def p_np_addConstInt(p):
    "np_addConstInt : "
    if p[-1] not in constants_table['Int'].keys():
        memory = p_get_constant_memory('Int')
        constants_table['Int'][p[-1]
                               ] = {'type': 'Int', 'memory': memory}
    terms_stack.append(constants_table['Int'][p[-1]]['memory'])
    types_stack.append('Int')


def p_np_addConstFloat(p):
    "np_addConstFloat : "
    if p[-1] not in constants_table['Float'].keys():
        memory = p_get_constant_memory('Float')
        constants_table['Float'][p[-1]] = {'type': 'Float', 'memory': memory}
    terms_stack.append(constants_table['Float'][p[-1]]['memory'])
    types_stack.append('Float')


def p_np_addConstChar(p):
    "np_addConstChar : "
    if p[-1] not in constants_table['Char'].keys():
        memory = p_get_constant_memory('Char')
        constants_table['Char'][p[-1]] = {'type': 'Char', 'memory': memory}
    terms_stack.append(constants_table['Char'][p[-1]]['memory'])
    types_stack.append('Char')

# INSTRUCTIONS

# - ERA Call


def p_np_call_era(p):
    'np_call_era : '
    global param_counter, curr_func_name, call_origin, operators_stack
    if p[-1] in variables_table.keys():
        param_counter = 0
        call_origin = curr_func_name
        curr_func_name = p[-1]
        operators_stack.append('(')
        quadruples.append(Quadruple('ERA', p[-1], None, None))
    else:
        p_notifError(str(lexer.lineno) +
                     " - The function " + p[-1] + " was not declared")

# - GOSUB Call


def p_np_call_gosub(p):
    'np_call_gosub : '
    global curr_func_name, prog_name, operators_stack, call_origin
    quadruples.append(Quadruple('GOSUB', curr_func_name, None, None))
    operators_stack.pop()

    # If it is not Void, assign result to the reserved memory space for that function
    if variables_table[curr_func_name]['type'] != 'Void':
        memory = variables_table[prog_name]['variables'][curr_func_name]['memory']
        if call_origin == prog_name:
            temp_memory = p_get_global_memory(
                variables_table[curr_func_name]['type'])
        else:
            temp_memory = p_get_local_memory(
                variables_table[curr_func_name]['type'])
        quadruples.append(Quadruple('=', memory, None, temp_memory))

        # Add term and type to use in expressions
        terms_stack.append(temp_memory)
        types_stack.append(variables_table[curr_func_name]['type'])


def p_np_isStatement(p):
    'np_isStatement : '
    global curr_func_name
    if variables_table[curr_func_name]['type'] != 'Void':
        p_notifError(str(lexer.lineno) + " - You cannot use the function " +
                     curr_func_name + " in a statement")
    curr_func_name = call_origin


def p_np_isExpression(p):
    'np_isExpression : '
    global curr_func_name
    if variables_table[curr_func_name]['type'] == 'Void':
        p_notifError(str(lexer.lineno) + " - You cannot use the function " +
                     curr_func_name + " in an expression")
    curr_func_name = call_origin

# - ...


def p_np_addOperator(p):
    'np_addOperator : '
    operators_stack.append(p[-1])


def get_memory_for_ID(type):
    if curr_func_name == prog_name:
        return p_get_global_memory(type)
    else:
        return p_get_local_memory(type)

# Global


def p_get_global_memory(type):
    global global_mem_int, global_mem_float, global_mem_char, variable_size
    if type == 'Int':
        if global_mem_int < 2000:
            global_mem_int += int(variable_size)
            return global_mem_int - int(variable_size) + 1
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of global integer variables")
    elif type == 'Float':
        if global_mem_float < 3000:
            global_mem_float += int(variable_size)
            return global_mem_float - int(variable_size) + 1
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of global float variables")
    elif type == 'Char':
        if global_mem_char < 4000:
            global_mem_char += int(variable_size)
            return global_mem_char - int(variable_size) + 1
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of global character variables")

# Local


def p_get_local_memory(type):
    global local_mem_int, local_mem_float, local_mem_char, variable_size
    if type == 'Int':
        if local_mem_int < 5000:
            local_mem_int += int(variable_size)
            return local_mem_int - int(variable_size) + 1
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of local integer variables")
    elif type == 'Float':
        if local_mem_float < 6000:
            local_mem_float += int(variable_size)
            return local_mem_float - int(variable_size) + 1
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of local float variables")
    elif type == 'Char':
        if local_mem_char < 7000:
            local_mem_char += int(variable_size)
            return local_mem_char - int(variable_size) + 1
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of local character variables")

# Constant


def p_get_constant_memory(type):
    global constant_mem_int, constant_mem_float, constant_mem_char
    if type == 'Int':
        if constant_mem_int < 8000:
            constant_mem_int += 1
            return constant_mem_int
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of integer constants")
    elif type == 'Float':
        if constant_mem_float < 9000:
            constant_mem_float += 1
            return constant_mem_float
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of float constants")
    elif type == 'Char':
        if constant_mem_char < 10000:
            constant_mem_char += 1
            return constant_mem_char
        else:
            p_notifError(str(lexer.lineno) +
                         " - Stack overflow of character constants")

# PERFORM OPERATIONS

# * /


def p_np_doTerm(p):
    'np_doTerm : '
    global operators_stack, terms_stack, curr_func_name
    if operators_stack:
        if operators_stack[-1] in ['*', '/']:
            right_side = terms_stack.pop()
            left_side = terms_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operators_stack.pop()

            result_type = SemanticCube.getCubeType(
                left_type, right_type, operator)
            if curr_func_name == prog_name:
                result_memory = p_get_global_memory(result_type)
            else:
                result_memory = p_get_local_memory(result_type)

            if result_type != 'Error':
                quadruples.append(
                    Quadruple(operator, left_side, right_side, result_memory))
                terms_stack.append(result_memory)
                types_stack.append(result_type)
            else:
                p_notifError(str(lexer.lineno) +
                             " - Type operation error")


# + -
def p_np_doExp(p):
    'np_doExp : '
    global operators_stack, terms_stack, curr_func_name
    if operators_stack:
        if operators_stack[-1] in ['+', '-']:
            right_side = terms_stack.pop()
            left_side = terms_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operators_stack.pop()

            result_type = SemanticCube.getCubeType(
                left_type, right_type, operator)
            if curr_func_name == prog_name:
                result_memory = p_get_global_memory(result_type)
            else:
                result_memory = p_get_local_memory(result_type)

            if result_type != 'Error':
                quadruples.append(
                    Quadruple(operator, left_side, right_side, result_memory))
                terms_stack.append(result_memory)
                types_stack.append(result_type)
            else:
                p_notifError(str(lexer.lineno) +
                             " - Type operation error")


# < > >= >= != ==
def p_np_doSuperExp(p):
    'np_doSuperExp : '
    global operators_stack, terms_stack, curr_func_name
    if operators_stack:
        if operators_stack[-1] in ['<', '>', '<=', '>=', '!=', '==']:
            right_side = terms_stack.pop()
            left_side = terms_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operators_stack.pop()

            result_type = SemanticCube.getCubeType(
                left_type, right_type, operator)
            if curr_func_name == prog_name:
                result_memory = p_get_global_memory(result_type)
            else:
                result_memory = p_get_local_memory(result_type)

            if result_type != 'Error':
                quadruples.append(
                    Quadruple(operator, left_side, right_side, result_memory))
                terms_stack.append(result_memory)
                types_stack.append(result_type)
            else:
                p_notifError(str(lexer.lineno) +
                             " - Type operation error")


# & |
def p_np_doHyperExp(p):
    'np_doHyperExp : '
    global operators_stack, terms_stack, curr_func_name
    if operators_stack:
        if operators_stack[-1] in ['&', '|']:
            right_side = terms_stack.pop()
            left_side = terms_stack.pop()
            right_type = types_stack.pop()
            left_type = types_stack.pop()
            operator = operators_stack.pop()

            result_type = SemanticCube.getCubeType(
                left_type, right_type, operator)
            if curr_func_name == prog_name:
                result_memory = p_get_global_memory(result_type)
            else:
                result_memory = p_get_local_memory(result_type)

            if result_type != 'Error':
                quadruples.append(
                    Quadruple(operator, left_side, right_side, result_memory))
                terms_stack.append(result_memory)
                types_stack.append(result_type)
            else:
                p_notifError(str(lexer.lineno) +
                             " - Type operation error")


def p_np_assignment(p):
    'np_assignment : '
    equal = operators_stack.pop()
    right = terms_stack.pop()
    left = terms_stack.pop()
    right_type = types_stack.pop()
    left_type = types_stack.pop()
    if right_type == left_type:
        quadruples.append(Quadruple(equal, right, None, left))
    else:
        p_notifError(str(lexer.lineno) +
                     " - Assignment cannot be performed due to type compatibility")


def p_np_read(p):
    'np_read : '
    global curr_func_name
    # Check if ID is among declared global or local variables
    if p[-1] in variables_table[curr_func_name]['variables'].keys():
        quadruples.append(Quadruple(
            'READ', None, None, variables_table[curr_func_name]['variables'][p[-1]]['memory']))
    elif p[-1] in variables_table[prog_name]['variables'].keys():
        quadruples.append(Quadruple(
            'READ', None, None, variables_table[prog_name]['variables'][p[-1]]['memory']))
    else:
        p_notifError(str(lexer.lineno) + " - Variable " +
                     p[-1] + " must be declared before it is used")


def p_np_write(p):
    'np_write : '
    global curr_func_name, prog_name, terms_stack
    quadruples.append(Quadruple('WRITE', None, None, terms_stack[-1]))


def p_np_string(p):
    'np_string : '
    global mem_strings, prog_name
    if p[-1] not in constants_table['string'].keys():
        mem_strings += 1
        constants_table['string'][p[-1]
                                  ] = {'type': 'string', 'memory': mem_strings}

    quadruples.append(Quadruple('WRITE', None, None, mem_strings))


def p_np_return(p):
    'np_return : '
    global curr_func_type, prog_name, returnExists
    if types_stack.pop() == curr_func_type:
        returnExists = 1
        quadruples.append(Quadruple('RETURN', None, None, terms_stack.pop()))
    else:
        p_notifError(str(lexer.lineno) +
                     " - The returned value is not compatible with the function type")


def p_np_startDecision(p):
    'np_startDecision : '
    if types_stack[-1] == 'Int' or types_stack[-1] == 'Float':
        quadruples.append(Quadruple('GOTOF', terms_stack[-1], None, 0))
        jumps_stack.append(len(quadruples)-1)
    else:
        p_notifError(str(lexer.lineno) + " - The variable " +
                     terms_stack[-1] + " can't be used for a decision")


def p_np_startDecisionElse(p):
    'np_startDecisionElse : '
    quadruples.append(Quadruple('GOTO', None, None, 0))
    quadruples[jumps_stack.pop()].res = len(quadruples)
    jumps_stack.append(len(quadruples)-1)


def p_np_endDecision(p):
    'np_endDecision : '
    quadruples[jumps_stack.pop()].res = len(quadruples)


def p_np_conditionalBefore(p):
    'np_conditionalBefore : '
    jumps_stack.append(len(quadruples))


def p_np_conditionalDuring(p):
    'np_conditionalDuring : '
    quadruples.append(Quadruple('GOTOF', terms_stack.pop(), None, 0))


def p_np_conditionalAfter(p):
    'np_conditionalAfter : '
    quadruples.append(Quadruple('GOTO', None, None, jumps_stack[-1]))
    quadruples[jumps_stack.pop() + 1].res = len(quadruples)


# NON CONDITIONAL
def p_np_addIDFor(p):
    'np_addIDFor : '
    global curr_func_name, prog_name
    if p[-1] in variables_table[curr_func_name]['variables'].keys():
        if variables_table[curr_func_name]['variables'][p[-1]]['type'] == 'Int':
            terms_stack.append(
                variables_table[curr_func_name]['variables'][p[-1]]['memory'])
            types_stack.append('Int')
        else:
            p_notifError(str(lexer.lineno) + " - Variable " +
                         p[-1] + " must be an integer.")
    elif p[-1] in variables_table[prog_name]['variables'].keys():
        if variables_table[prog_name]['variables'][p[-1]]['type'] == 'Int':
            terms_stack.append(
                variables_table[prog_name]['variables'][p[-1]]['memory'])
            types_stack.append('Int')
        else:
            p_notifError(str(lexer.lineno) + " - The variable " +
                         p[-1] + " must be an integer to be used in a non-conditional loop")
    else:
        p_notifError(str(lexer.lineno) + " - The variable " +
                     p[-1] + " was not declared in the non-conditional loop")


def p_np_for_assignment(p):
    'np_for_assignment : '
    global curr_assignment_for
    equal = operators_stack.pop()
    right = terms_stack.pop()
    left = terms_stack.pop()
    quadruples.append(Quadruple(equal, right, None, left))
    curr_assignment_for = left


def p_np_boolFor(p):
    'np_boolFor : '
    global curr_assignment_for

    right_side = terms_stack.pop()
    left_side = curr_assignment_for
    right_side_type = types_stack.pop()
    left_side_type = 'Int'
    operator = '<'

    result_type = SemanticCube.getCubeType(
        left_side_type, right_side_type, operator)
    if curr_func_name == prog_name:
        memory_result = p_get_global_memory(result_type)
    else:
        memory_result = p_get_local_memory(result_type)

    if result_type != 'Error':
        quadruples.append(Quadruple(operator, left_side,
                          right_side, memory_result))
        jumps_stack.append(len(quadruples)-1)
        quadruples.append(Quadruple('GOTOF', memory_result, None, 0))
    else:
        p_notifError(str(lexer.lineno) + " - Error in type operations")
    for_var_stack.append(curr_assignment_for)


def p_np_endCondition(p):
    'np_endCondition  : '
    global curr_assignment_for
    curr_assignment_for = for_var_stack.pop()

    if '1' not in constants_table['Int'].keys():
        constants_table['Int']['1'] = {
            'type': 'Int', 'memory': p_get_constant_memory('Int')}
    memory_sum = constants_table['Int']['1']['memory']

    if curr_func_name == prog_name:
        memory_result = p_get_global_memory('Int')
    else:
        memory_result = p_get_local_memory('Int')

    quadruples.append(Quadruple('+', curr_assignment_for,
                      memory_sum, memory_result))
    quadruples.append(Quadruple('=', memory_result, None, curr_assignment_for))
    quadruples.append(Quadruple('GOTO', None, None, jumps_stack[-1]))
    quadruples[jumps_stack.pop() + 1].res = len(quadruples)

# CALL


def p_np_sentParam(p):
    'np_sentParam : '
    global param_counter, curr_func_name
    param_counter += 1

    # if a nth record exists in the parameter table
    if param_counter in variables_table[curr_func_name]['parameters'].keys():
        # if the type matches
        if variables_table[curr_func_name]['parameters'][param_counter] == types_stack.pop():
            if curr_func_name not in function_params.keys():
                function_params[curr_func_name] = {}
            function_params[curr_func_name][terms_stack[-1]] = None

            quadruples.append(
                Quadruple('PARAM', terms_stack.pop(), None, "PARAM"+str(param_counter)))
        else:
            p_notifError(str(lexer.lineno) + " - The parameters of the function " +
                         curr_func_name + " do not match in their types")
    else:
        p_notifError(str(lexer.lineno) + " - The amount of parameters of the function " +
                     curr_func_name + " do not match with those of its call")


def p_np_receiveParams(p):
    'np_receiveParams : '
    global param_receive_counter

    # If the variable that receives a function as a parameter does not exist in its local context and is not global
    if p[-3] not in variables_table[curr_func_name]['variables'].keys() and p[-3] not in variables_table[prog_name]['variables'].keys():
        memory = get_memory_for_ID(p[-1])
        variables_table[curr_func_name]['variables'][p[-3]
                                                     ] = {'type': p[-1], 'memory': memory}

        # Add types to variable table to check when parameters are sent from a call
        if len(variables_table[curr_func_name]['parameters']) == 0:
            param_receive_counter = 0
        param_receive_counter += 1
        variables_table[curr_func_name]['parameters'][param_receive_counter] = p[-1]
    else:
        p_notifError(str(lexer.lineno) + " - The variable " +
                     p[-3] + " was previously declared")

# Validates the specific case if no parameters are sent and if they were expected


def p_np_paramValidation(p):
    'np_paramValidation : '
    if len(variables_table[curr_func_name]['parameters']) != param_counter:
        p_notifError(str(lexer.lineno) + " - The amount of parameters of the function " +
                     curr_func_name + " do not match with those of its call")


# CLEAR STACKS
def p_np_emptyStacks(p):
    'np_emptyStacks : '
    global terms_stack, operators_stack, types_stack
    terms_stack.clear()
    operators_stack.clear()
    types_stack.clear()


def p_notifError(errorText):
    'notifError : '
    print("\n! Line " + errorText + "\n")
    sys.exit()


parser = yacc.yacc()


def generate_data():
    try:
        file = input('File: ')
        with open(file, 'r') as file:
            parser.parse(file.read())

            print("\nVARIABLE TABLE ->")
            print(variables_table)

            print("\nCONSTANT TABLE ->")
            print(constants_table)

            print("\nFUNCTION PARAMETERS ->")
            print(function_params)

            counter = 0
            print("\nQUADRUPLES ->")
            for item in quadruples:
                print(str(counter) + " " + str(item.getQuadruple()))
                counter += 1

    except EOFError:
        print("Error")


# Function to be run from the virtual machine


def run_vm():
    generate_data()

    data = {
        'quadruples': quadruples,
        'variable_table': variables_table,
        'constant_table': constants_table,
        'prog_name': prog_name,
        'function_parameters': function_params
    }

    return data
