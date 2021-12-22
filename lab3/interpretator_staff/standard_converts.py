import sys


class Var:
    def __init__(self, type_="UNDEF", value_=None, left_=False, right_=False):
        self.left = left_
        self.right = right_
        if value_ == "UNDEF":
            value_ = None
        self.type = type_
        if type_ == "LOGIC":
            match value_:
                case "FALSE":
                    self.value = False
                case "TRUE":
                    self.value = True
                case _:
       #             print("strange logic moment")
                    self.value = value_
        else:
            self.value = value_

    def __repr__(self):
        if self.type == 'STRING' and self.value is not None:
            return f'{self.type},"{self.value}"'
        else:
            return f'{self.type},{self.value}'


class Conversion:
    def __init__(self):
        self.custom_converts = list()

    def converting(self, var, type_):
        if var is None:
            print("wtf")
        match type_:
            case var.type:
                return var
            case 'LOGIC':
                if var.type == 'NUMERIC':
                    return self.num_to_logic(var)
                if var.type == 'STRING':
                    return self.string_to_logic(var)
            case 'NUMERIC':
                if var.type == 'LOGIC':
                    return self.logic_to_num(var)
                if var.type == 'STRING':
                    return self.string_to_num(var)
            case 'STRING':
                if var.type == 'LOGIC':
                    return self.logic_to_string(var)
                if var.type == 'NUMERIC':
                    return self.num_to_string(var)
            case 'UNDEF':
                return var
            case _:
                print("Необъявленное преобразование")

    @staticmethod
    def logic_to_num(value):
        match value.value:
            case ('TRUE' | True):
                return Var('NUMERIC', 1)
            case ('FALSE' | False):
                return Var('NUMERIC', 0)
            case 'UNDEF':
                return Var('NUMERIC', 'UNDEF')
            case _:
                sys.stderr.write(f'Unknown conversion\n')

    @staticmethod
    def num_to_logic(value):
        if int(value.value) == 0:
            return Var('LOGIC', False)
        elif isinstance(value.value, int):
            return Var('LOGIC', True)
        elif value.value == 'UNDEF':
            return Var('LOGIC', 'UNDEF')
        else:
            sys.stderr.write(f'Illegal conversion\n')

    @staticmethod
    def string_to_logic(value):
        match value.value:
            case "true":
                return Var('LOGIC', bool(True))
            case ('UNDEF' | None):
                return Var('LOGIC', None)
            case _:
                return Var('LOGIC', bool(False))

    @staticmethod
    def logic_to_string(value):
        return Var('STRING', str(value.value))

    @staticmethod
    def string_to_num(value):
        if len(value.value) == 1:
            return Var('NUMERIC', ord(value.value))
        else:
            return Var('NUMERIC', 0)

    @staticmethod
    def num_to_string(value):
        return Var('STRING', str(value.value))

