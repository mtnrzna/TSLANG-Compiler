import ply.lex as lex
from compiler_levels.lexer.tokens import *


lexer = lex.lex()

def tokenize(data):
    lexer.input(data)
    for tok in lexer:
        print(tok.value, tok.type)
