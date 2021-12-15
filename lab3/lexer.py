import sys
import ply.lex as lex

reserved = {
    # just for normal programm
    'TRUE': 'TRUE',
    'FALSE': 'FALSE',
    'LOGIC': 'LOGIC',
    'NUMERIC': 'NUMERIC',
    'STRING': 'STRING',
    'UNDEF': 'UNDEF',
    'RECORD': 'RECORD',
    'DATA': 'DATA',
    'CONVERSION': 'CONVERSION',
    'TO': 'TO',
    'FROM': 'FROM',
    'BLOCK': 'BLOCK',
    'UNBLOCK': 'UNBLOCK',
    'PROC': 'PROC',
    # specialForRobot
    'MOVEUP': 'MOVEUP',
    'MOVEDOWN': 'MOVEDOWN',
    'MOVERIGHT': 'MOVERIGHT',
    'MOVELEFT': 'MOVELEFT',
    'PINGUP': 'PINGUP',
    'PINGDOWN': 'PINGDOWN',
    'PINGRIGHT': 'PINGRIGHT',
    'PINGLEFT': 'PINGLEFT',
    'VISION': 'VISION',
    'VOICE': 'VOICE'
}


class Lexer(object):
    def __init__(self):
        self.lexer = lex.lex(module=self)

    tokens = list(reserved.values()) + ['DECIMAL', 'VARIABLE',
              'ASSIGNMENT', 'PLUS', 'MINUS',
              'STAR', 'SLASH', 'CARET',
              'LESS', 'GREATER', 'EQ', 'NOTEQ',
              'R_RBRACKET', 'L_RBRACKET',
              'R_QBRACKET', 'L_QBRACKET',
              'R_FBRACKET', 'L_FBRACKET',
              'AMPERSAND', 'COMMA', 'DOT', 'TEXT', 'LINE']

    precedence = (
        ('right', 'ASSIGNMENT'),
        ('left', 'LESS', 'GREATER', 'EQ', 'NOTEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'STAR', 'SLASH'),
        ('right', 'CARET'),
        ('right', 'UMINUS'),
    )

    t_ASSIGNMENT = r'\='
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_STAR = r'\*'
    t_SLASH = r'\/'
    t_CARET = r'\^'
    t_LESS = r'\<'
    t_GREATER = r'\>'
    t_EQ = r'\?'
    t_NOTEQ = r'\!'
    t_R_RBRACKET = r'\)'
    t_L_RBRACKET = r'\('
    t_R_QBRACKET = r'\]'
    t_L_QBRACKET = r'\['
    t_R_FBRACKET = r'\}'
    t_L_FBRACKET = r'\{'
    t_AMPERSAND = r'\&'
    t_COMMA = r'\,'
    t_DOT = r'\.'

    t_ignore = ' \t'

    def t_comment(self, t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'VARIABLE')
        return t

    def t_TEXT(self, t):
        r'".*?"'
        t.value = t.value[1:len(t.value)-1]
        return t

    def t_DECIMAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_LINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    def t_error(self, t):
        sys.stderr.write(f'Illegal character: {t.value[0]} at line {t.lexer.lineno}\n')
        t.lexer.skip(1)

    def input(self, info):
        return self.lexer.input(info)

    def token(self):
        return self.lexer.token()


if __name__ == '__main__':
    data1 = '''NUMERIC = 1232432'''
    data2 = '''STRING = "qwerty"
    //hucif owyovby8fowy8ov f8oqe'''
    data3 = '''
    NUMERIC a = 1324321
    a = b + c - a + gfd
    '''
    lexer = Lexer()
    lexer.input(data3)
    while True:
        token = lexer.token()
        if token is None:
            break
        else:
            print(f"Line[{token.lineno}]: position[{token.lexpos}]: type = '{token.type}'\tvalue = '{token.value}'")
