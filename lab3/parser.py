import ply.yacc as yacc
from ply.lex import LexError
import sys
from typing import List, Dict
from lexer import Lexer
from my_ast import Node


class Parser(object):

    tokens = Lexer.tokens
    precedence = Lexer.precedence

    def __init__(self):
        self.correct = True
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
        self._procedures: Dict[str, Node] = dict()
        self._records: Dict[str, Node] = dict()
        self._conversions: Dict[str, Node] = dict()

    def parse(self, s) -> List:
        try:
            res = self.parser.parse(s)
            return [res,  self.correct]
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n')

    def get_procedures(self):
        return self._procedures

    def get_records(self):
        return self._records

    def get_conversations(self):
        return self._conversions

    @staticmethod
    def p_program(p):
        """program : statements"""
        p[0] = Node(type_='program', child_=p[1], line_number_=p.lineno(1), position_=p.lexpos(1))

    @staticmethod
    def p_statements(p):
        """statements : statements statement
                      | statement"""
        if len(p) == 3:
            p[0] = Node(type_='statements', child_=[p[1], p[2]])
        else:
            p[0] = Node(type_='statements', child_=[p[1]])


    @staticmethod
    def p_statement(p):
        """statement : declaration LINE
                     | call LINE
                     | procedure LINE
                     | record LINE
                     | assignment LINE
                     | while LINE
                     | command LINE
                     | empty LINE"""
        p[0] = p[1]


    @staticmethod
    def p_name(p):
        """name : NAME indexing
                | NAME"""
        match len(p):
            case 3:
                p[0] = Node(type_='component_of', value_=p[1], child_=p[2], line_number_=p.lineno(1), position_=p.lexpos(1))
            case _:
                p[0] = Node(type_='name', value_=p[1])

    @staticmethod
    def p_type(p):
        """type : NUMERIC
                | STRING
                | LOGIC
                | NAME"""
        p[0] = p[1]

    @staticmethod
    def p_declaration(p):
        """declaration : type name"""
        p[0] = Node(type_='declaration', value_=p[1], child_=p[2])

    @staticmethod
    def p_call(p):
        """call : NAME L_RPAREN names R_RPAREN"""
        p[0] = Node(type_='procedure_call', value_=p[1], child_=p[3])

    @staticmethod
    def p_assignment(p):
        """assignment : name ASSIGNMENT expression
                      | name ASSIGNMENT assignment"""
        p[0] = Node(type_='assignment', value_=p[1], child_=p[3], line_number_=p.lineno(1), position_=p.lexpos(1))

    @staticmethod
    def p_while(p):
        """ while : L_FPAREN expression R_FPAREN BLOCK internal_statements UNBLOCK"""
        p[0] = Node('while', child_={'condition': p[2], 'body': p[5]})

    @staticmethod
    def p_command(p):
        """command : MOVEUP      L_RPAREN name R_RPAREN
                   | MOVEDOWN    L_RPAREN name R_RPAREN
                   | MOVERIGHT   L_RPAREN name R_RPAREN
                   | MOVELEFT    L_RPAREN name R_RPAREN
                   | PINGUP      L_RPAREN name R_RPAREN
                   | PINGDOWN    L_RPAREN name R_RPAREN
                   | PINGRIGHT   L_RPAREN name R_RPAREN
                   | PINGLEFT    L_RPAREN name R_RPAREN
                   | VISION      L_RPAREN name R_RPAREN
                   | VOICE       L_RPAREN expression R_RPAREN"""
        p[0] = Node(type_='command', value_=p[1], child_=p[3], line_number_=p.lineno(1), position_=p.lexpos(1))

    def p_procedure(self, p):
        """procedure : PROC NAME L_QPAREN parameters R_QPAREN statements_group"""
        self._procedures[p[2]] = Node(type_='procedure', value_=p[2], child_={'parameters': p[4], 'body': p[6]})
        p[0] = Node(type_='procedure_description', value_=p[2], line_number_=p.lineno(1), position_=p.lexpos(1))

    def p_record(self, p):
        """record : RECORD NAME DATA L_QPAREN parameters R_QPAREN
                  | RECORD NAME DATA L_QPAREN parameters R_QPAREN conversions"""
        if len(p) == 7:
            self._records[p[2]] = Node(type_='record', value_=p[2], child_={'parameters': p[5], 'conversions': None})
        else:
            self._records[p[2]] = Node(type_='record', value_=p[2], child_={'parameters': p[5], 'conversions': p[7]})
        p[0] = Node(type_='record_description', value_=p[2], line_number_=p.lineno(1), position_=p.lexpos(1))

    @staticmethod
    def p_conversions(p):
        """conversions :  conversions conversion
                       | conversion"""
        match len(p):
            case 3:
                p[0] = Node(type_='conversions', child_=[p[1], p[2]])
            case _:
                p[0] = Node(type_='conversions', child_=[p[1]])

    @staticmethod
    def p_conversion(p):
        """conversion : CONVERSION TO   type NAME
                      | CONVERSION FROM type NAME"""
        p[0] = Node(type_='conversion', value_=p[2], child_=[p[3], p[4]])

    @staticmethod
    def p_empty(p):
        """empty : """
        pass


    @staticmethod
    def p_expression(p):
        """expression : name
                      | const
                      | full_expression"""
        p[0] = p[1]

    @staticmethod
    def p_names(p):
        """names :  expression
                 |  expression COMMA names """
        match len(p):
            case 2:
                p[0] = Node(type_='names', child_=p[1])
            case _:
                p[0] = Node(type_='names', child_=[p[1], p[3]])


    # @staticmethod
    # def p_name(p):
    #     """name : NAME indexing
    #             | NAME"""
    #     match len(p):
    #         case 3:
    #             p[0] = Node(type_='component_of', value_=p[1], child_=p[2],
    #             line_number_=p.lineno(1), position_=p.lexpos(1))
    #         case _:
    #             p[0] = Node(type_='name', value_=p[1])


    @staticmethod
    def p_indexing(p):
        """indexing : L_QPAREN DECIMAL R_QPAREN indexing
                    | L_QPAREN DECIMAL R_QPAREN
                    | L_QPAREN NAME R_QPAREN indexing
                    | L_QPAREN NAME R_QPAREN"""
        if len(p) == 5:
            p[0] = Node(type_='indexing', value_=p[2], child_=p[4], line_number_=p.lineno(2), position_=p.lexpos(2))
        else:
            p[0] = Node(type_='indexing', value_=p[2], line_number_=p.lineno(2), position_=p.lexpos(2))

    @staticmethod
    def p_const(p):
        """const : TRUE
                 | FALSE
                 | UNDEF
                 | DECIMAL
                 | TEXT
                 """
        p[0] = Node(type_='const', value_=p[1])

    @staticmethod
    def p_full_expression(p):
        """full_expression : part_expression PLUS    part_expression   %prec PLUS
                              | part_expression MINUS   part_expression   %prec MINUS
                              | part_expression STAR    part_expression   %prec STAR
                              | part_expression SLASH   part_expression   %prec SLASH
                              | part_expression CARET   part_expression   %prec CARET
                              | part_expression GT part_expression   %prec GT
                              | part_expression LT    part_expression   %prec LT
                              | part_expression EQ      part_expression   %prec EQ
                              | part_expression NE   part_expression   %prec NE
                              | MINUS expression %prec UMINUS"""
        match len(p):
            case 4:
                p[0] = Node(type_='binary_expression', value_=p[2], child_=[p[1], p[3]], line_number_=p.lineno(1),
                        position_=p.lexpos(1))
            case _:
                p[0] = Node(type_='unary_expression', value_=p[1], child_=p[2], line_number_=p.lineno(1),
                        position_=p.lexpos(1))

    @staticmethod
    def p_part_expression_right(p):
        """part_expression : DOT expression"""
        p[0] = Node(type_='part_expression', value_='right', child_=p[2], line_number_=p.lineno(1),
                    position_=p.lexpos(1))

    @staticmethod
    def p_part_expression_left(p):
        """part_expression : expression DOT"""
        p[0] = Node(type_='part_expression', value_='left', child_=p[1], line_number_=p.lineno(1),
                    position_=p.lexpos(1))

    @staticmethod
    def p_part_expression(p):
        """part_expression : expression"""
        p[0] = Node(type_='part_expression', value_=None, child_=p[1], line_number_=p.lineno(1), position_=p.lexpos(1))

    @staticmethod
    def p_parameters(p):
        """parameters : parameter COMMA parameters
                      | parameter"""
        match len(p):
            case 2:
                p[0] = Node(type_='parameters', child_=[p[1]])
            case _:
                p[0] = Node(type_='parameters', child_=[p[1], p[3]])

    @staticmethod
    def p_parameter(p):
        """parameter : declaration AMPERSAND
                     | declaration"""
        match len(p):
            case 2:
                p[0] = Node(type_='parameter', value_=p[1])
            case _:
                p[0] = Node(type_='ref_parameter', value_=p[1])

    @staticmethod
    def p_statements_group(p):
        """statements_group : BLOCK internal_statements UNBLOCK
                            | internal_statement"""
        match len(p):
            case 4:
                p[0] = p[2]
            case _:
                p[0] = p[1]

    @staticmethod
    def p_internal_statements(p):
        """internal_statements :  internal_statement internal_statements
                            | internal_statement"""
        match len(p):
            case 3:
                p[0] = Node(type_='statements', child_=[p[1], p[2]])
            case _:
                p[0] = Node(type_='statements', child_=[p[1]])

    @staticmethod
    def p_internal_statement(p):
        """internal_statement : declaration LINE
                           | assignment LINE
                           | while LINE
                           | command LINE
                           | call LINE
                           | empty LINE"""
        p[0] = p[1]



    def p_error(self, p):
        try:
            sys.stderr.write(f'Syntax error at {p.lineno} line\n')
        except:
            sys.stderr.write(f'Syntax error\n')
        self.correct = False




if __name__ == '__main__':
    data1 = '''NUMERIC myNum
    myNum = 1232432
    '''
    data2 = '''STRING myStr
     myStr = "qwerty"
    //hucif owyovby8fowy8ov f8oqe'''
    data3 = '''
    NUMERIC a = 1324321
    a = b + c - a + gfd
    '''
    f = open("tests/fibonacci.txt")
    data4 = f.read()
    f.close()

    f = open("tests/fibonacci_recursion.txt")
    data5 = f.read()
    f.close()

    f = open("tests/bubble.txt")
    data6 = f.read()
    f.close()

    f = open("tests/just_test")
    data7 = f.read()
    f.close()

    parser = Parser()
    tree, fl = parser.parse(data4)
    print('Code tree: ')
    tree.print()
    print('Procedures: ')
    print(parser.get_procedures())