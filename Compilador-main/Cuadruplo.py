class Cuadruplo:
    def __init__(self, operador, operando1, operando2, resultado):
        self.operador = operador
        self.operando1 = operando1
        self.operando2 = operando2
        self.resultado = resultado

    def getCuad(self):
        return str(self.operador) + " " + str(self.operando1) + " " + str(self.operando2) + " " + str(self.resultado)
