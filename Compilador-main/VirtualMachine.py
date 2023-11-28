import sys
import re
import Yacc
import math
import pickle

with open('dirFunc.pkl', 'rb') as f:
    dirFunc = pickle.load(f)

with open('Constants.pkl', 'rb') as f:
    auxConstants = pickle.load(f)

with open('Quadruples.pkl', 'rb') as f:
    Quadruples = pickle.load(f)


currentLevel = 0
breadCrumbs = []
currentFunction = []
pointers = {}
pointVals = {}
Constants = {}

# Memory
intMemory = [{}]
floatMemory = [{}]
charMemory = [{}]
boolMemory = [{}]



for key, info in auxConstants.items():
    Constants[info['dir']] = key


def updateMemory(dir, val):
    print(f"Before update: {intMemory}")
    if dir >= 1000 and dir < 2000:
        intMemory[currentLevel][dir] = math.floor(val)
    elif dir >= 2000 and dir < 3000:
        floatMemory[currentLevel][dir] = val
    elif dir >= 3000 and dir < 4000:
        charMemory[currentLevel][dir] = val
    elif dir >= 4000 and dir < 5000:
        boolMemory[currentLevel][dir] = val
    elif dir >= 5000 and dir < 6000:
        intMemory[currentLevel][dir] = math.floor(val)
    elif dir >= 6000 and dir < 7000:
        floatMemory[currentLevel][dir] = val
    elif dir >= 7000 and dir < 8000:
        charMemory[currentLevel][dir] = val
    elif dir >= 8000 and dir < 9000:
        boolMemory[currentLevel][dir] = val
    elif dir >= 9000 and dir < 10000:
        intMemory[currentLevel][dir] = math.floor(val)
    elif dir >= 10000 and dir < 11000:
        floatMemory[currentLevel][dir] = val
    elif dir >= 11000 and dir < 12000:
        charMemory[currentLevel][dir] = val
    elif dir >= 12000 and dir < 13000:
        boolMemory[currentLevel][dir] = val
    elif dir >= 13000 and dir < 14000:
        intMemory[currentLevel][dir] = math.floor(val)
    elif dir >= 14000 and dir < 15000:
        floatMemory[currentLevel][dir] = val
    elif dir >= 15000 and dir < 16000:
        charMemory[currentLevel][dir] = val
    elif dir >= 16000 and dir < 17000:
        boolMemory[currentLevel][dir] = val
    elif dir >= 17000 and dir < 18000:
        if Quadruples[currentCuad][2] == '':
            realVal = pointers[dir]
            pointVals[realVal] = math.floor(val)
        elif Quadruples[currentCuad][2] != '':
            pointers[dir] = val
            if val not in pointVals:
                pointVals[val] = None
    elif dir >= 18000 and dir < 19000:
        if Quadruples[currentCuad][2] == '':
            realVal = pointers[dir]
            pointVals[realVal] = val
        elif Quadruples[currentCuad][2] != '':
            pointers[dir] = val
            if val not in pointVals:
                pointVals[val] = None
    print(f"After update: {intMemory}")  # Debug statement
                
def get_val(dir, currentLevel):
    print(f"intMemory before getting value: {intMemory}")  # Debug statement
    dierction = int(dir)
    print(dierction)
    if dierction >= 1000 and dierction < 2000:
        val = intMemory[currentLevel][dierction]
    elif dierction >= 2000 and dierction < 3000:
        val = floatMemory[currentLevel][dierction]
    elif dierction >= 3000 and dierction < 4000:
        val = charMemory[currentLevel][dierction]
    elif dierction >= 4000 and dierction < 5000:
        val = boolMemory[currentLevel][dierction]
    elif dierction >= 5000 and dierction < 6000:
        val = intMemory[currentLevel][dierction]
    elif dierction >= 6000 and dierction < 7000:
        val = floatMemory[currentLevel][dierction]
    elif dierction >= 7000 and dierction < 8000:
        val = charMemory[currentLevel][dierction]
    elif dierction >= 8000 and dierction < 9000:
        val = boolMemory[currentLevel][dierction]
    elif dierction >= 9000 and dierction < 10000:
        val = Constants[dierction]
    elif dierction >= 10000 and dierction < 11000:
        val = Constants[dierction]
    elif dierction >= 11000 and dierction < 12000:
        val = Constants[dierction]
    elif dierction >= 12000 and dierction < 13000:
        val = Constants[dierction]
    elif dierction >= 13000 and dierction < 14000:
        val = intMemory[currentLevel][dierction]
    elif dierction >= 14000 and dierction < 15000:
        val = floatMemory[currentLevel][dierction]
    elif dierction >= 15000 and dierction < 16000:
        val = charMemory[currentLevel][dierction]
    elif dierction >= 16000 and dierction < 17000:
        val = boolMemory[currentLevel][dierction]
    elif dierction >= 17000 and dierction < 18000:
        val = Constants[dierction]
    elif dierction >= 18000 and dierction < 19000:
        aux = pointers[dierction]
        val = pointVals[aux]
    elif dierction >= 19000 and dierction < 20000:
        aux = pointers[dierction]
        val = pointVals[aux]
        
    if val is None:
        print(f"Error: uninitialized variable {dir}")
        sys.exit(1)

    return val

currentCuad = 0

while(Quadruples[currentCuad][0] != 'ENDPROC'):
    if(Quadruples[currentCuad][0] == 'GOTO'):
        currentCuad = Quadruples[currentCuad][3]
    elif(Quadruples[currentCuad][0] == '|'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)
        res = left or right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '&'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)
        res = left and right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '<'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)
        res = left < right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '>'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)
        res = left > right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '<='):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)
        res = left <= right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '>='):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)
        res = left >= right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '=='):
        print(f"currentLevel before getting value: {currentLevel}")  # Debug statement
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)
        res = left == right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '+'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)

        res = left + right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '-'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)

        res = left - right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '*'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)

        res = left * right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '/'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        right = get_val(Quadruples[currentCuad][2], currentLevel)

        res = left / right
        updateMemory(Quadruples[currentCuad][3], res)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == '='):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        updateMemory(Quadruples[currentCuad][3], left)
        currentCuad += 1
        
    elif(Quadruples[currentCuad][0] == 'GOTOF'):
        left = get_val(Quadruples[currentCuad][1], currentLevel)
        if(not left):
            currentCuad = Quadruples[currentCuad][3]
        else:
            currentCuad += 1
    
    elif(Quadruples[currentCuad][0] == 'PRINT'):
        left = get_val(Quadruples[currentCuad][3], currentLevel)
        print(left)
        currentCuad += 1
    elif(Quadruples[currentCuad][0] == 'READ'):
        address = Quadruples[currentCuad][3]
        val = input()
        if(address >= 1000 and address < 2000):
            valaux = int(val)
            updateMemory(address, valaux)
        elif(address >= 2000 and address < 3000):
            valaux = float(val)
            updateMemory(address, valaux)
        elif(address >= 3000 and address < 4000):
            valaux = str(val)
            updateMemory(address, valaux)
        elif(address >= 4000 and address < 5000):
            valaux = bool(val)
            updateMemory(address, valaux)
        elif(address >= 5000 and address < 6000):
            valaux = int(val)
            updateMemory(address, valaux)
        elif(address >= 6000 and address < 7000):
            valaux = float(val)
            updateMemory(address, valaux)
        elif(address >= 7000 and address < 8000):
            valaux = str(val)
            updateMemory(address, valaux)
        elif(address >= 8000 and address < 9000):
            valaux = bool(val)
            updateMemory(address, valaux)
        currentCuad += 1
    elif(Quadruples[currentCuad][0] == 'ERA'):
        intMemory.append({})
        floatMemory.append({})
        charMemory.append({})
        boolMemory.append({})
        currentFunction.append(Quadruples[currentCuad][3])
        currentCuad += 1
    elif(Quadruples[currentCuad][0] == 'PARAM'):
        left = get_val(Quadruples[currentCuad][2], currentLevel)
        currentLevel += 1
        updateMemory(Quadruples[currentCuad][3], left)
        currentLevel -= 1

        currentCuad += 1
    elif(Quadruples[currentCuad][0] == 'GOSUB'):
        breadCrumbs.append(currentCuad + 1)
        jump = dirFunc[Quadruples[currentCuad][3]]['Start_dir']
        currentCuad = jump
        currentLevel += 1
    elif(Quadruples[currentCuad][0] == 'return'):
        left = get_val(Quadruples[currentCuad][3], currentLevel)
        func = currentFunction[-1]
        func_var_address = dirFunc['global']['vars'][func]['dir']
        auxCurrLevel = currentLevel
        currentLevel -= 1
        updateMemory(func_var_address, left)
        currentLevel = auxCurrLevel
        currentCuad += 1
    elif(Quadruples[currentCuad][0] == 'ENDFUNC'):
        
        currentCuad = breadCrumbs.pop()
        del intMemory[currentLevel]
        del floatMemory[currentLevel]
        del charMemory[currentLevel]
        del boolMemory[currentLevel]
        currentFunction.pop()
        currentLevel -= 1
    elif(Quadruples[currentCuad][0] == 'VER'):
        valEntrada = get_val(Quadruples[currentCuad][2], currentLevel)
        valLimite = get_val(Quadruples[currentCuad][3], currentLevel)
        if(valEntrada < 0 or valEntrada >= valLimite):
            print("Index out of bounds")
            sys.exit()
        currentCuad += 1
        
    