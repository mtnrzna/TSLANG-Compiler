from compiler_levels.lexer.tokens import *


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