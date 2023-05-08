from SemanticCube import SEMANTIC_CUBE


class Quadruple:
    def __init__(self):
        self.operator = None
        self.left_operand = None
        self.right_operand = None
        self.result = None

    def create_quadruple(self, operator, left_operand, right_operand, result):
        if left_operand.type not in SEMANTIC_CUBE[operator][right_operand.type]:
            raise TypeError(
                f"Invalid operation: {left_operand.type} {operator} {right_operand.type}")

        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
        return self

    def get_operator(self):
        return self.operator

    def set_operator(self, operator):
        self.operator = operator

    def get_left_operand(self):
        return self.left_operand

    def set_left_operand(self, left_operand):
        self.left_operand = left_operand

    def get_right_operand(self):
        return self.right_operand

    def set_right_operand(self, right_operand):
        self.right_operand = right_operand

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result
