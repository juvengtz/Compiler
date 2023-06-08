# IMPORTS
import sys
import re
import Yacc
from Quadruple import *

# GLOBAL VARIABLES

current_quadruple = 0
running = 1
operator = 'OP'
current_function = '...'
function_call_stack = []
current_parameters = []
local_variables = []
local_table_dictionary = {}

data = Yacc.run_vm()

quadruples = data['quadruples']
variable_table = data['variable_table']
constant_table = data['constant_table']
prog_name = data['prog_name']
function_parameters = data['function_parameters']

super_variable_table = {}
super_constant_table = {}

max_integer = 1000
min_integer = 2001
for var in variable_table[prog_name]['variables']:
    if variable_table[prog_name]['variables'][var]['type'] == 'Int':
        if variable_table[prog_name]['variables'][var]['memory'] > max_integer:
            max_integer = variable_table[prog_name]['variables'][var]['memory']

        if variable_table[prog_name]['variables'][var]['memory'] < min_integer:
            min_integer = variable_table[prog_name]['variables'][var]['memory']

while min_integer <= max_integer:
    super_variable_table[min_integer] = None
    min_integer += 1

max_float = 2000
min_float = 3001
for var in variable_table[prog_name]['variables']:
    if variable_table[prog_name]['variables'][var]['type'] == 'Float':
        if variable_table[prog_name]['variables'][var]['variable_table'] > max_float:
            max_float = variable_table[prog_name]['variables'][var]['variable_table']

        if variable_table[prog_name]['variables'][var]['variable_table'] < min_float:
            min_float = variable_table[prog_name]['variables'][var]['variable_table']

while min_float <= max_float:
    super_variable_table[min_float] = None
    max_float += 1

max_char = 3000
min_char = 4001

for var in variable_table[prog_name]['variables']:
    if variable_table[prog_name]['variables'][var]['type'] == 'Char':
        if variable_table[prog_name]['variables'][var]['memory'] > max_char:
            max_char = variable_table[prog_name]['variables'][var]['memory']

        if variable_table[prog_name]['variables'][var]['memory'] < min_char:
            min_char = variable_table[prog_name]['variables'][var]['memory']

while min_char <= max_char:
    super_variable_table[min_char] = None
    min_char += 1

# super_constant_table = {}
for type_ in constant_table:
    for var in constant_table[type_]:
        super_constant_table[constant_table[type_][var]['memory']] = var

# SUPER TABLE

st = {**super_variable_table, **super_constant_table}

# HELPERS


def notify_error(error_text):
    print("\n! ERROR - " + error_text + "\n")
    sys.exit()


def get_type(memory):
    if re.match("\(\d+\)", str(memory)):
        memory = get_type(int(memory[1:-1]))
    memory = int(memory)
    # INTEGER
    if 1001 <= memory <= 2000 or 4001 <= memory <= 5000 or 7001 <= memory <= 8000:
        if 4001 <= memory <= 5000:
            return int(local_variables[-1][memory])
        else:
            return int(st[memory])
    # FLOAT
    elif 2001 <= memory <= 3000 or 5001 <= memory <= 6000 or 8001 <= memory <= 9000:
        if 5001 <= memory <= 6000:
            return float(local_variables[-1][memory])
        else:
            return float(st[memory])
    # CHARACTERS
    elif 3001 <= memory <= 4000 or 6001 <= memory <= 7000 or 9001 <= memory <= 10000:
        if 6001 <= memory <= 7000:
            return local_variables[-1][memory]
        else:
            return st[memory]
    # STRINGS
    elif 10001 <= memory <= 11000:
        text = st[memory]
        size = len(text)
        return text[1:size-1]
    else:
        notify_error("OPERATION ERROR")


def start_local_memory(funcName):
    global local_table_dictionary
    local_table_dictionary.clear()
    for local_var in variable_table[funcName]['variables']:
        local_table_dictionary[variable_table[funcName]
                               ['variables'][local_var]['memory']] = None


def delete_local_memory():
    global local_variables
    local_variables.pop()


def is_local(memory):
    if re.match("\(\d+\)", str(memory)):
        memory = get_type(int(memory[1:-1]))

    if 4001 <= memory <= 7000:
        return True
    else:
        return False


def comparer(bool, memory):
    global current_quadruple
    if is_local(memory):
        if bool == False:
            local_variables[-1][memory] = 0
        else:
            local_variables[-1][memory] = 1
    else:
        if bool == False:
            st[memory] = 0
        else:
            st[memory] = 1
    current_quadruple += 1


def reading_caster(value, memory):
    if re.match("[-]?[0-9]+([.][0-9]+)", value):
        if 2001 <= memory <= 3000 or 5001 <= memory <= 6000 or 8001 <= memory <= 9000:
            return float(value)
        else:
            notify_error("Provided value does not match the variable's type")
    elif re.match("[-]?[0-9]+", value):
        if 1001 <= memory <= 2000 or 4001 <= memory <= 5000 or 7001 <= memory <= 8000:
            return int(value)
        else:
            notify_error("Provided value does not match the variable's type")
    elif re.match("([^\'])", value):
        if 3001 <= memory <= 4000 or 6001 <= memory <= 7000 or 9001 <= memory <= 10000:
            return value
        else:
            notify_error("Provided value does not match the variable's type")
    else:
        notify_error("The read value cannot be assigned to the variable")


# QUADRUPLE ANALYSIS
while running:
    quadruple = Quadruple.getQuadruple(quadruples[current_quadruple])
    operator = quadruple[0]
    # GOTO / GOTOF
    if operator == 'GOTO':
        current_quadruple = quadruple[3]
    elif operator == 'GOTOF':
        if get_type(quadruple[1]) == 0 or get_type(quadruple[1]) == 0.0:
            current_quadruple = quadruple[3]
        else:
            current_quadruple += 1

    # ASSIGNMENT
    elif operator == '=':

        a = quadruple[3]
        b = get_type(quadruple[1])

        if re.match("\(\d+\)", str(a)):
            a = get_type(int(a[1:-1]))

        if is_local(a):
            local_variables[-1][a] = b
        else:
            st[a] = b
        current_quadruple += 1

    # OPERATIONS
    elif operator in ('+', '-', '*', '/'):

        # print(f'quadruple[1]: {quadruple[1]}, quadruple[2]: {quadruple[2]}')
        res = eval(
            f'{get_type(quadruple[1])} {operator} {get_type(quadruple[2])}')

        # Division by zero
        if operator == '/' and get_type(quadruple[2]) == 0:
            notify_error("Division by zero is being performed")

        if is_local(quadruple[3]):
            local_variables[-1][quadruple[3]] = res
        else:
            st[quadruple[3]] = res
        current_quadruple += 1

    # COMPARATORS
    elif operator in ('<', '>', '<=', '>=', '==', '!='):

        res = eval(
            f'{get_type(quadruple[1])} {operator} {get_type(quadruple[2])}')
        comparer(res, quadruple[3])
        """if is_local(quadruple[3]):
            if res == False:
                local_variables[-1][quadruple[3]] = 0
            else:
                local_variables[-1][quadruple[3]] = 1
        else:
            if quadruple[3] == False:
                st[quadruple[3]] = 0
            else:
                st[quadruple[3]] = 1
        current_quadruple += 1 """

    # AND
    elif operator == '&':

        res1, res2 = (get_type(quadruple[i]) != 0 for i in (1, 2))
        if is_local(quadruple[3]):
            local_variables[-1][quadruple[3]] = int(res1 + res2 == 2)
        else:
            st[quadruple[3]] = int(res1 + res2 == 2)
        current_quadruple += 1

    # OR
    elif operator == '|':

        res1, res2 = (get_type(quadruple[i]) != 0 for i in (1, 2))

        if is_local(quadruple[3]):
            local_variables[-1][quadruple[3]] = int(res1 + res2 != 0)
        else:
            st[quadruple[3]] = int(res1 + res2 != 0)
        current_quadruple += 1

    # WRITE
    elif operator == 'WRITE':

        print(get_type(quadruple[3]))
        current_quadruple += 1

    elif operator == 'READ':

        var = input("> ")
        if is_local(quadruple[3]):
            local_variables[-1][quadruple[3]
                                ] = reading_caster(var, quadruple[3])
        else:
            st[quadruple[3]] = reading_caster(var, quadruple[3])
        current_quadruple += 1
    elif operator == 'ERA':

        start_local_memory(quadruple[1])
        current_function = quadruple[1]
        current_parameters = list(
            variable_table[current_function]['variables'])
        current_quadruple += 1
    elif operator == 'PARAM':

        index = int((quadruple[3])[5]) - 1
        local_table_dictionary[variable_table[current_function]['variables']
                               [current_parameters[index]]['memory']] = get_type(quadruple[1])
        current_quadruple += 1
    elif operator == 'GOSUB':

        function_call_stack.append(current_quadruple)
        local_variables.append(local_table_dictionary)
        local_table_dictionary = {}
        current_quadruple = variable_table[quadruple[1]]['quadrupleNum']
    elif operator == 'RETURN':

        memory = variable_table[prog_name]['variables'][current_function]['memory']
        st[memory] = get_type(quadruple[3])
        delete_local_memory()
        current_quadruple = int(function_call_stack.pop()) + 1
    elif operator == 'ENDFUNC':

        delete_local_memory()
        current_quadruple = int(function_call_stack.pop()) + 1
    elif operator == 'VERIFY':

        if int(quadruple[2]) <= int(get_type(quadruple[1])) < int(quadruple[3]):
            pass
        else:
            notify_error("Invalid index for array/matrix")
        current_quadruple += 1
    elif operator == 'SUM_BASE':

        res = int(quadruple[1]) + get_type(quadruple[2])
        if is_local(res):
            local_variables[-1][quadruple[3]] = res
        else:
            st[quadruple[3]] = res
        current_quadruple += 1
    elif operator == 'END':

        running = 0
    else:
        print("Error in the quadruples")
        running = 0
