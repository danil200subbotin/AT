

# coding=utf8
import ply.lex as lex
import re
import AppClass

tokens = (
    'TARGET', 'COLON', 'SPACE', 'EOS',
)

t_TARGET = r'[\.\_A-Za-z][\w\.\_]*'
t_COLON = r':'
t_EOS = r'\n+'
t_SPACE = r'[\t ]+'

t_ignore = ''

#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += len(t.value)

def t_error(t):
  #  print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    raise Exception('I do not know Python!')

lexer = lex.lex(reflags=re.UNICODE | re.DOTALL | re.IGNORECASE)






if __name__=="__main__":
    data = '''
:f 27 
jk:s  
u:c  
bF: eH 
y:iT J 
5F: d1 
:i xr 
:5 q. 
l:m W 
: T4 
H8:Vs nX 
b9:3Z sc
  
    '''
    allTokens = []
    lexer.input(data)

    while True:
        try:
            tok = lexer.token() # читаем следующий токен
            if not tok:
                break      # закончились печеньки
            allTokens.append(tok)
       #     print(tok)
        except Exception as error:
      #      print("поймал ошибку лексер")
            allTokens.append(None)

    test = AppClass.AppClass()
    test.CheckFile(allTokens)
   # print(allTokens[0].lineno)

    print(chr(80))









