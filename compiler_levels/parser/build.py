import ply.yacc as yacc
from compiler_levels.lexer.tokens import *
from compiler_levels.parser.grammer import *


parser = yacc.yacc(debug=True)

def parse(data):
    parser.parse(data)

