import copy
import sys
from typing import Dict

import numpy as np

import robot as rb
from interpretator_staff.standard_converts import Var, Conversion
from interpretator_staff.standard_operations import Operations
from my_ast import Node
from parser import Parser

debug = False


class Exit(Exception):
    pass


# Item of symbol table

class Interpreter:

    def __init__(self, _parser=Parser(), window=None):
        self.window = window
        self.program = None
        self.standard_conversions = Conversion()
        self.standard_operations = Operations()
        self.parser = _parser
        self.notion_table = None
        self.custom_conversions: Dict[str, Node] = dict()   #str == "<from>_to_<to>"
        self.namespace_id = 0
        self.fatal_error = False
        self.find_exit = False
        self.ast = None
        self.procedures: Dict[str, Node] = dict()
        self.records: Dict[str, Node] = dict()
        self.robot = rb.Robot()

    def interpreter(self, program=None):
        self.program = program
        self.notion_table = [dict()]
        self.ast, _correctness = self.parser.parse(self.program)
        if _correctness:
            print("pasring success")
            if debug:
                print("Program tree:")
                self.ast.print()
                print("\n")
            self.interpreter_node(self.ast)
        else:
            sys.stderr.write(f'Can\'t intemperate incorrect input file\n')

    def interpreter_node(self, node):

        if self.robot.found_exit:  # ---------------------------------------
            raise Exit

        if node is None:
            return

        match node.type:

            case 'program':
                try:
                    self.interpreter_node(node.child)
                except Exit:
                    print("Все закрыл!!!!!! Получил нужный результат")
                    pass

            case 'statements':
                for child in node.child:
                    try:
                        self.interpreter_node(child)
                    except Exit:
                        raise Exit

            case 'error':
                sys.stderr.write(f'UNEXPECTED ERROR\n')

            case 'declaration':
                type_ = node.value
                child_ = node.child
                if (type_ in ['NUMERIC', 'LOGIC', 'STRING']) or (type_ in self.records):
                    if child_.type == 'component_of':
                        array_index = child_.child.value
                        if isinstance(array_index, str):
                            array_index = (self.get_variable(array_index)).value
                        result = list()
                        if type_ in self.records:
                            elem = [type_, copy.deepcopy(self.records[type_][0])]
                            raise Exit
                        else:
                            elem = Var(type_)
                        for i in range(array_index):
                            result.append(copy.deepcopy(elem))
                        type_ = ["ARRAY", type_]
                        self.declare_array(child_.value, type_, np.array(result))
                    else:
                        self.declare_variable(child_, type_)
                else:
                    sys.stderr.write(f'Невозможный тип для переменной или записи\n')

            case 'record_description':
                recordName = node.value
                if recordName in self.records.keys():
                    sys.stderr.write(f'Попытка перезаписать запись\n')
                elif (recordName in self.procedures.keys()) or (
                        recordName in self.notion_table[self.namespace_id].keys()):
                    sys.stderr.write(f'Попытка назвать запись именем существующей процедуры\n')
                else:
                    self.records[recordName] = self.add_new_record(self.parser.get_records()[recordName])

            case 'procedure_description':
                if node.value in self.procedures.keys():
                    sys.stderr.write(f'Can\'t redeclare the procedure\n')
                elif (node.value in self.procedures.keys()) or (
                        node.value in self.notion_table[self.namespace_id].keys()):
                    sys.stderr.write(f'Can\'t declare the procedure: name is taken\n')
                else:
                    self.procedures[node.value] = self.parser.get_procedures()[node.value]

            case 'procedure_call':
                if not (node.value in self.procedures.keys()):
                    sys.stderr.write(f'Попытка вызвать необъявленную процедуру\n')
                else:
                    self.run_procedure(node)

            case 'assignment':
                name = node.value.value
                if (name not in self.notion_table[self.namespace_id].keys()) and (name not in self.records):
                    print("1")
                    sys.stderr.write(f'Unknown name for assignment\n')
                    raise

                expression = self.interpreter_node(node.child)

                if isinstance(self.notion_table[self.namespace_id][name], Var):
                    result = self.notion_table[self.namespace_id][name]
                elif node.value.type == 'component_of':
                    result = self.notion_table[self.namespace_id][name]
                    index_ = node.value.child
                    while not isinstance(index_, list):
                        result = result[1]
                        if isinstance(result, dict) and isinstance(index_.value, str):
                            result = result[index_.value]
                        else:
                            if isinstance(index_.value, str):
                                result = result[(self.get_variable(index_.value)).value]
                            else:
                                result = result[index_.value]
                        index_ = index_.child
                elif isinstance(node.value.child, dict):
                    result = self.notion_table[self.namespace_id][name]
                    if isinstance(expression, list):
                        if result[0] == expression[0]:
                            result[1] = copy.deepcopy(expression[1])
                        else:
                            sys.stderr.write(f'DIFFERENT TYPES FOR RECORDS ARE ILLEGAL YET\n')
                        return expression
                    else:
                        index_ = node.value.child
                        while index_:
                            if 'ARRAY' in result[0]:
                                index_ = node.value.child
                                if isinstance(index_.value, str):
                                    index_ = (self.get_variable(index_)).value
                                else:
                                    index_ = index_.value
                                result = self.notion_table[self.namespace_id][name][1]
                                result = result[index_]
                                self.assign(result, expression)
                                return expression
                else:
                    if isinstance(node.value.child, list):
                        result = self.notion_table[self.namespace_id][name][1]
                        if isinstance(expression, np.ndarray):
                            for i in range(min(len(result), len(expression))):
                                self.assign(result[i], expression[i])
                        else:
                            for i in range(len(result)):
                                self.assign(result[i], expression)
                        return expression
                    else:
                        index_ = node.value.child
                        if isinstance(index_.value, str):
                            index_ = (self.get_variable(index_)).value
                        else:
                            index_ = index_.value
                        result = self.notion_table[self.namespace_id][name][1]
                        result = result[index_]
                        self.assign(result, expression)
                        return expression
                self.assign(result, expression)
                return expression

            case 'while':
                while self.standard_conversions.converting(self.interpreter_node(node.child['condition']), 'LOGIC').value:
                    self.interpreter_node(node.child['body'])

            case 'command':
                name = node.child.value
                expression = None
                if name not in self.notion_table[self.namespace_id].keys():
                    sys.stderr.write(f'Undeclared variable2\n')
                else:
                    expression = self.notion_table[self.namespace_id][name]
                    if type(self.notion_table[self.namespace_id][name]) == Var:
                        pass
                    elif node.child.type == 'component_of':
                        index_ = node.child.child
                        while not isinstance(index_, list):
                            expression = expression[1]
                            if isinstance(expression, dict) and isinstance(index_.value, str):
                                expression = expression[index_.value]
                            else:
                                if isinstance(index_.value, str):
                                    expression = expression[(self.get_variable(index_.value)).value]
                                else:
                                    expression = expression[index_.value]
                            index_ = index_.child
                if node.value == 'MOVEUP':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.move_up(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'MOVEDOWN':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.move_down(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'MOVERIGHT':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.move_right(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'MOVELEFT':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.move_left(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'PINGUP':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.ping_up(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'PINGDOWN':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.ping_down(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'PINGRIGHT':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.ping_right(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'PINGLEFT':
                    if expression.type == 'NUMERIC':
                        expression.value = self.robot.ping_left(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'VISION':
                    if isinstance(expression, list):
                        if expression[0][1] == 'STRING':
                            pasws = self.robot.vision()
                            for i in range(len(pasws)):
                                expression[1][i].value = pasws[i]
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                elif node.value == 'VOICE':
                    if expression.type == 'STRING':
                        self.robot.voice(expression.value)
                    else:
                        sys.stderr.write(f'ILLEGAL COMMAND PARAMETER TYPE\n')
                else:
                    sys.stderr.write(f'UNEXPECTED ERROR')


            case 'unary_expression':
                expression = self.interpreter_node(node.child)
                if expression.value is None:
                    return Var(expression.type)
                else:
                    if expression.type == 'NUMERIC':
                        return Var('NUMERIC', -expression.value)
                    elif expression.type == 'LOGIC':
                        return Var('LOGIC', not expression.value)
                    else:
                        sys.stderr.write(f'Illegal operation: illegal type\n')
                        return Var()

            case 'binary_expression':
                result = None
                exp1 = self.interpreter_node(node.child[0])
                exp2 = self.interpreter_node(node.child[1])
                match node.value:
                    case '+':
                        result = self.standard_operations.binary_plus(exp1, exp2,
                                                                      standard_conversions=self.standard_conversions)
                    case '-':
                        result = self.standard_operations.bin_minus(exp1, exp2,
                                                                    standard_conversions=self.standard_conversions)
                    case '*':
                        result = self.standard_operations.bin_multi(exp1, exp2,
                                                                    standard_conversions=self.standard_conversions)
                    case '/':
                        result = self.standard_operations.bin_slash(exp1, exp2,
                                                                    standard_conversions=self.standard_conversions)
                    case '^':
                        result = self.standard_operations.bin_caret(exp1, exp2,
                                                                    standard_conversions=self.standard_conversions)
                    case '>':
                        result = self.standard_operations.bin_greater(exp1, exp2,
                                                                      standard_conversions=self.standard_conversions)
                    case '<':
                        result = self.standard_operations.bin_less(exp1, exp2,
                                                                   standard_conversions=self.standard_conversions)
                    case '?':
                        result = self.standard_operations.bin_equal(exp1, exp2,
                                                                    standard_conversions=self.standard_conversions)
                    case '!':
                        result = self.standard_operations.bin_not_equal(exp1, exp2,
                                                                        standard_conversions=self.standard_conversions)
                if type(exp1) == Var:
                    if exp1.right:
                        result.right = True
                    if exp2.left:
                        result.left = True
                return result

            case 'part_expression':
                expression = self.interpreter_node(node.child)
                if type(expression) == Var:
                    if expression:
                        if node.value:
                            if node.value == "right":
                                expression.right = True
                                if debug:
                                    print('right up')
                            elif node.value == "left":
                                expression.left = True
                                if debug:
                                    print('left up')
                else:
                    for elem in expression:
                        if node.value:
                            if node.value == "right":
                                elem.right = True
                                if debug:
                                    print('right up')
                            elif node.value == "left":
                                elem.left = True
                                if debug:
                                    print('left up')
                return expression

            case 'const':
                value = node.value
                if (str(value)).isdigit():
                    return Var('NUMERIC', int(value))
                match value:
                    case ('TRUE' | 'FALSE' | True | False):
                        return Var('LOGIC', value)
                    case ('UNDEF' | None):
                        return Var('UNDEF', None)
                    case _:
                        return Var('STRING', value)

            case 'name':
                return self.get_value(node)

            case 'component_of':
                return self.get_component(node)

    # for assign
    def assign(self, variable: Var, expression: Var):
        if expression is None:
            return
        expression = self.standard_conversions.converting(expression, variable.type)
        if expression:
            if variable.type == expression.type:
                variable.value = expression.value
            elif expression.type == 'UNDEF':
                variable.value = None
        else:
            variable.value = None

    def declare_variable(self, node, _type):            # ---------------------------------------------------------
        if node.type == 'name':
            if (node.value in self.records.keys()) or (node.value in self.procedures.keys()) or (
                    node.value in self.notion_table[self.namespace_id].keys()):
                sys.stderr.write(f'The name is already taken\n')
            else:
                _value = node.value
                if _type in ['NUMERIC', 'LOGIC', 'STRING']:
                    self.notion_table[self.namespace_id][_value] = Var(_type, None)
                elif _type in self.records.keys():
                    # print(_type, copy.deepcopy(self.records[_type].child['parameters']))
                    self.notion_table[self.namespace_id][_value] = [_type, copy.deepcopy(self.records[_type].child['parameters'])]
            return

    def declare_array(self, _name, _type, _value):          # ---------------------------------------------------------
        if (_name in self.records.keys()) or (_name in self.procedures.keys()) or (
                _name in self.notion_table[self.namespace_id].keys()):
            sys.stderr.write(f'The name is already taken\n')
        else:
            self.notion_table[self.namespace_id][_name] = [_type, _value]
        return

    def get_value(self, node, sc=None):                 # ---------------------------------------------------------
        if sc is None:
            sc = self.namespace_id
        if node.type == 'name':
            return self.get_variable(node.value, sc)
        elif node.type == 'component_of':
            return self.get_component(node, sc)
        else:
            sys.stderr.write(f'Illegal value\n')
        return Var()

    def get_variable(self, name, sc=None):                      # ---------------------------------------------------------
        if sc is None:
            sc = self.namespace_id
        if name in self.notion_table[sc].keys():
            if type(self.notion_table[sc][name]) == Var:
                return copy.copy(self.notion_table[sc][name])
            elif isinstance(self.notion_table[sc][name], list):
                return self.notion_table[sc][name]
            else:
                return self.notion_table[sc][name]
        else:
            sys.stderr.write(f' Namespace {sc}: Undeclared variable3\n')
        return Var()

    def get_component(self, node, sc=None):             # ---------------------------------------------------------
        if sc is None:
            sc = self.namespace_id
        if node.type == 'component_of':
            if node.value in self.notion_table[sc].keys():
                res = self.notion_table[sc][node.value]
                index = node.child
                n = 0
                while not isinstance(index, list):
                    if debug:
                        print(n, ' ', res)
                        n += 1
                    if isinstance(res, list):
                        res = res[1]
                    if debug:
                        print('->', n, ' ', res)
                    if type(index.value) == int:
                        if index.value not in range(len(res)):
                            sys.stderr.write(f'Out of index range\n')
                            return Var()
                        else:
                            if not isinstance(res, dict):
                                res = res[index.value]
                            else:
                                sys.stderr.write(f'Index instead of field name\n')
                                return Var()
                    else:
                        if index.value in self.notion_table[sc].keys():
                            if type(self.notion_table[sc][index.value]) == Var:
                                res = res[
                                    self.standard_conversions.converting(self.notion_table[sc][index.value], 'NUMERIC').value]
                            else:
                                new_array = []
                                def_var = copy.deepcopy(res[0])
                                def_var.value = None
                                index_array = self.notion_table[sc][index.value][1]
                                for i in range(len(index_array)):
                                    num = self.standard_conversions.converting(index_array[i], 'NUMERIC').value
                                    if num in range(len(res)):
                                        new_array.append(copy.deepcopy(res[num]))
                                    else:
                                        new_array.append(def_var)
                                res = np.array(new_array)
                                # return res
                        else:
                            if index.value in res.keys():
                                res = res[index.value]
                                # return res
                            else:
                                sys.stderr.write(f'Illegal data field\n')
                    index = index.child
                return res
            else:
                sys.stderr.write(f'Незадекларированный массив\n')
        else:
            sys.stderr.write(f'Illegal value\n')
        return Var()

    def run_procedure(self, node):                          # ---------------------------------------------------------
        self.notion_table.append(dict())
        self.namespace_id += 1
        data = node.child.child
        params = self.procedures[node.value].child['parameters'].child
        if debug:
            print('DATA: ', data)
            print('PAR: ', params)
        code = self.procedures[node.value].child['body']
        i = 0
        name = None
        res = None              # вероятно, придется удалить эту строку
        ref_arr = dict()
        while params and data:
            if isinstance(data, list):
                if data[0]:
                    res = self.get_value(data[0], self.namespace_id - 1)
                    if debug:
                        print('GOT VAL', res)
                name = [data[0].value]
                if data[0].type == 'component_of':
                    indexing = data[0].child.value
                    if not type(indexing) == int:
                        indexing = self.get_variable(indexing, self.namespace_id - 1).value
                    name.append(indexing)
                data = data[len(data) - 1]
            else:
                name = [data.value]
                if data.type == 'names':
                    pass
                else:
                    if type(data) == Node:
                        res = self.get_value(data, self.namespace_id - 1)
                    if data.type == 'component_of':
                        indexing = data.child.value
                        if not type(indexing) == int:
                            indexing = self.get_variable(indexing, self.namespace_id - 1).value
                        name.append(indexing)
                        data = data.child
                data = data.child
            if isinstance(params, list):
                self.interpreter_node(params[0].value)
                if params[0].type == 'ref_parameter':
                    ref_arr[params[0].value.child.value] = name
                self.notion_table[self.namespace_id][params[0].value.child.value] = copy.deepcopy(res)
                params = params[len(params) - 1]
            else:
                params = params.child
            i += 1
        for var in self.notion_table[self.namespace_id]:
            if var in ref_arr.keys():
                if len(ref_arr[var]) == 2:
                    self.notion_table[self.namespace_id - 1][ref_arr[var][0]][1][ref_arr[var][1]] = \
                        self.notion_table[self.namespace_id][var]
                else:
                    self.notion_table[self.namespace_id - 1][ref_arr[var][0]] = self.notion_table[self.namespace_id][
                        var]
        if debug:
            print(self.notion_table[self.namespace_id])
        self.interpreter_node(code)
        if debug:
            print(self.notion_table[self.namespace_id])
        self.notion_table.pop()
        self.namespace_id -= 1
        return

    def add_new_record(self, node):
        leftArgument = ""
        rightArgument = ""
        recordType = node.value
        self.namespace_id += 1
        self.notion_table.append(dict())
        p_params = node.child['parameters']
        p_convs = node.child['conversions']
        res_params = dict()
        res_convs = dict()
        while p_params:
            if isinstance(p_params, list):
                self.interpreter_node(p_params[0].value)
                res_params[p_params[0].value.child.value] = self.notion_table[self.namespace_id].pop(p_params[0].value.child.value)
                p_params = p_params[len(p_params) - 1]
            else:
                p_params = p_params.child

        if p_convs is not None:
            if len(p_convs.child) == 2:
                while len(p_convs.child) == 2:
                    match p_convs.child[1].value:
                        case "FROM":
                            rightArgument = recordType
                            leftArgument = p_convs.child[1].child[0]
                        case "TO":
                            leftArgument = recordType
                            rightArgument = p_convs.child[1].child[0]
                    res_convs[str(str(leftArgument) + "_to_" + str(rightArgument))] = p_convs.child[1]
                    p_convs = p_convs.child[0]
            match p_convs.child[0].value:
                case "FROM":
                    rightArgument = recordType
                    leftArgument = p_convs.child[0].child[0]
                case "TO":
                    rightArgument = p_convs.child[0].child[0]
                    leftArgument = recordType
            # print(p_convs.child[0])
            res_convs[str(str(leftArgument) + "_to_" + str(rightArgument))] = p_convs.child[0]
        self.notion_table.pop()
        self.namespace_id -= 1

        # добавляю свои преобразования
        if len(res_convs) != 0:
            for conv in res_convs:
                if res_convs[conv].child[1] in self.procedures:
                    procNode = self.procedures[res_convs[conv].child[1]]
                    res_convs[conv] = procNode
                else:
                    sys.stderr.write(f'You have to initialize the procedure {res_convs[conv].child[1]}\n')

            self.custom_conversions = (self.custom_conversions | res_convs)
        return Node(type_='record', value_=node.value, child_={'parameters': res_params, 'conversions': res_convs})
  # return res_params, res_convs

    def read_map_document(self, file_name):
        fl = open(file_name)
        _text = fl.readlines()
        robot_position = _text.pop(0).rstrip().split(" ")
        map_size = _text.pop(0).rstrip().split(" ")

        # robot set
        x = int(robot_position[0])
        y = int(robot_position[1])
        _map = [0] * int(map_size[0])

        for i in range(int(map_size[0])):
            _map[i] = [0] * int((map_size[1]))
        for i in range(int(map_size[0])):
            for j in range(int(map_size[1])):
                _map[i][j] = rb.MapCell("EMPTY")
        pos = 0
        for i in range(int(map_size[0])):
            line = list(_text.pop(0).rstrip())
            line = [rb.MapCell(rb.types[i]) for i in line]
            _map[pos] = line
            pos += 1
        while len(_text) > 0:
            password_info = _text.pop(0).rstrip().split(" ")
            passw = password_info[4]

            wall_x = int(password_info[0])
            wall_y = int(password_info[1])
            _map[wall_x][wall_y].passwords.append(passw)

            exit_x = int(password_info[2])
            exit_y = int(password_info[3])
            _map[exit_x][exit_y].passwords.append(passw)
        self.robot = rb.Robot(_x=x, _y=y, _map=_map, window=self.window)



