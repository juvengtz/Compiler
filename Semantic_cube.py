class SemanticCube:
    def getCubeType(type1, type2, op):

        if type1 == "Int":
            if type2 == "Int":
                return "Int"
            elif type2 == "Float":
                if op == "+" or op == "-" or op == "*" or op == "/":
                    return "Float"
                else:
                    return "Int"
            elif type2 == "Char":
                return "Error"

        if type1 == "Float":
            if type2 == "Int" or type2 == "Float":
                if op == "+" or op == "-" or op == "*" or op == "/":
                    return "Float"
                else:
                    return "Int"
            elif type2 == "Char":
                return "Error"

        if type1 == "Char":
            if type2 == "Int" or type2 == "Float":
                return "Error"
            elif type2 == "Char":
                if op == "==" or op == "!=":
                    return "Int"
                else:
                    return "Error"

        return "Error"
