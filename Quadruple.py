from SemanticCube import SEMANTIC_CUBE


class Quadruple:
    def __init__(self):
        self.operator = None
        self.left_operand = None
        self.right_operand = None
        self.result = None

    def create_quadruple(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
        return self
