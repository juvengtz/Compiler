class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def getQuadruple(self):
        return [self.operator, self.left_operand, self.right_operand, self.result]
