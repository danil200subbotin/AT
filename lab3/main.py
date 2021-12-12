from lexer import Lexer

text_input = """Logic a
a = true
Numeric b[10]
Numeric counter
Numeric x
b[1] = 13278194
counter = 1
BLOCK
    { b[1] > 0 } BLOCK
        x = counter 
        counter = counter + 1 + x
        print(x)
    UNBLOCK
UNBLOCK    
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)


for token in tokens:
    print(token)
