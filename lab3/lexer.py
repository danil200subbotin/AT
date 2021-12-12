from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('BLOCK', r'BLOCK')
        self.lexer.add('UNBLOCK', r'UNBLOCK')

        self.lexer.add('LOGIC', r'Logic')
        self.lexer.add('NUMERIC', r'Numeric')
        self.lexer.add('STRING', r'String')
        self.lexer.add('RECORD', r'Record')

        self.lexer.add('DATA', r'Data')

        self.lexer.add('CONVERSION TO', r'conversation to')
        self.lexer.add('CONVERSION FROM', r'conversation from')

        self.lexer.add('PRINT', r'print')
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_PAREN_S', r'\[')
        self.lexer.add('CLOSE_PAREN_S', r'\]')
        self.lexer.add('OPEN_PAREN_F', r'\{')
        self.lexer.add('CLOSE_PAREN_F', r'\}')
        self.lexer.add('SEMI_COLON', r'\;')

        self.lexer.add('ASSIGN', r'\=')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('DIGIT', r'\d+')

        self.lexer.add('MULTI', r'\*')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('DIVISION', r'\\')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('EXPONENTIATION', r'\^')

        self.lexer.add('BT', r'\>')
        self.lexer.add('LT', r'\<')
        self.lexer.add('EQ', r'\?')
        self.lexer.add('NE', r'\!')

        self.lexer.add('STRING_LITERAL', r'\"([\d\D])*\"')

        self.lexer.add('UNDEF', r'undef')

        self.lexer.add('TRUE', r'true')
        self.lexer.add('FALSE', r'false')

        self.lexer.add('LINE', r'\n')
        self.lexer.ignore(r'(\t|\ )+')

        self.lexer.add('IDENT', r'[a-zA-Z][a-zA-Z_0-9]*')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
