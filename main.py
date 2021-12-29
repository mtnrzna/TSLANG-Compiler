import ply.lex as lex
import ply.yacc as yacc

# List of token names.   This is always required
reserved = {
    'function': 'FUNCTION',
    'returns': 'RETURNS',
    'end': 'END',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'foreach': 'FOREACH',
    'of': 'OF',
    'return': 'RETURN',
    'val': 'VAL',
    'Int': 'INT',
    'Array': 'ARRAY',
    'Nil': 'NIL'
}

tokens = [
    'ID',
    'NUMBER',
    'EQUAL_EQUAL',  # ==
    'EXCL_EQUAL',  # !=
    'SMALL_EQUAL',  # <=
    'BIG_EQUAL',  # >=
    'PIPE_PIPE',  # !!
    'AMP_AMP',  # &&
    'EQUAL',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'PERCENT',
    'SMALL',  # <
    'BIG',  # >
    'QUEST_MARK',  # ?
    'EXCL_MARK',  # !
    'COLON',
    'SEMICOLON',
    'COMMA',
    'LBRACKET',  # [
    'RBRACKET',  # ]
    'LPARANT',  # (
    'RPARANT',  # )
    ] + list(reserved.values())

# Regular expression rules for simple tokens
t_EQUAL_EQUAL = r'=='
t_EXCL_EQUAL = r'!='
t_SMALL_EQUAL = r'<='
t_BIG_EQUAL = r'>='
t_PIPE_PIPE = r'\|\|'
t_AMP_AMP = r'&&'
t_EQUAL = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_PERCENT = r'%'
t_SMALL = r'<'
t_BIG = r'>'
t_QUEST_MARK = r'\?'
t_EXCL_MARK = r'!'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPARANT = r'\('
t_RPARANT = r'\)'


# A regular expression rule with some action code
def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# Comment: defining a token rule that returns no value
def t_COMMENT(t):
    r"""--[^\n]*\n"""  # $ is for when the code ends with a comment
    pass


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# File
file = open("code.txt", "r")
data = file.read()

# Build the lexer
lexer = lex.lex()

lexer.input(data)

# Tokenize
'''while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)'''
for tok in lexer:
    print(tok.value, tok.type)


#  Parser

# Grammars for parser

def p_prog(p):
    '''prog : func
            | func prog'''
    print('rule 0 reduced')


def p_func(p):
    '''func : FUNCTION ID LPARANT flist RPARANT RETURNS type COLON body END'''
    print('rule 1 reduced')


def p_body(p):
    '''body : stmt
            | stmt body'''
    print('rule 2 reduced')


def p_stmt(p):
    '''stmt : expr SEMICOLON
            | defvar SEMICOLON
            | IF LPARANT expr RPARANT stmt
            | IF LPARANT expr RPARANT stmt ELSE stmt
            | WHILE LPARANT expr RPARANT DO stmt
            | FOREACH LPARANT ID OF expr RPARANT stmt
            | RETURN expr SEMICOLON
            | COLON body END'''
    print('rule 3 reduced')


def p_defvar(p):
    '''defvar : VAL type ID'''
    print('rule 4 reduced')


def p_expr(p):
    '''expr : ID LPARANT clist RPARANT
            | expr LBRACKET expr RBRACKET
            | expr QUEST_MARK expr COLON expr
            | expr EQUAL expr
            | expr PLUS expr
            | expr MINUS expr
            | expr MULTIPLY expr
            | expr DIVIDE expr
            | expr PERCENT expr
            | expr SMALL expr
            | expr BIG expr
            | expr EQUAL_EQUAL expr
            | expr EXCL_EQUAL expr
            | expr SMALL_EQUAL expr
            | expr BIG_EQUAL expr
            | expr PIPE_PIPE expr
            | expr AMP_AMP expr
            | EXCL_MARK expr
            | MINUS expr
            | PLUS expr
            | LPARANT expr RPARANT
            | ID
            | NUMBER'''
    print('rule 5 reduced')


def p_flist(p):
    '''flist :
            | type ID
            | type ID COMMA flist'''
    print('rule 6 reduced')


def p_clist(p):
    '''clist :
            | expr
            | expr COMMA clist'''
    print('rule 7 reduced')


def p_type(p):
    '''type : INT
            | ARRAY
            | NIL'''


#def p_empty(p):
#    '''empty :'''
#    pass


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

#Set up precedence
precedence = (
    ('left', 'AMP_AMP', 'EXCL_MARK', 'PIPE_PIPE', 'SMALL_EQUAL', 'BIG_EQUAL', 'EXCL_EQUAL', 'EQUAL_EQUAL', 'SMALL', 'BIG'),
    ('left', 'EQUAL', 'QUEST_MARK', 'COLON'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'PERCENT'),
    ('left', 'LPARANT', 'RPARANT', 'LBRACKET', 'RBRACKET')
)
# Build the parser
parser = yacc.yacc(debug=True)

parser.parse()

