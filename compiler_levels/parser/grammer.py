import config
from compiler_levels.lexer.tokens import *
from utils.abstract_tree import create_node
from utils.show_tree import show_tree
from utils.symbol_table import SymbolTable


def p_prog(p):
    '''prog : func
            | func prog'''
    print(f"rule 0 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "prog"
    p[0] = create_node(p)
    config.syntax_tree = p[0]


def p_func(p):
    '''func : FUNCTION ID LPARANT flist RPARANT RETURNS type COLON body END'''
    print(f"rule 1 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "func"
    p[0] = create_node(p)


def p_body(p):
    '''body : stmt
            | stmt body'''
    print(f"rule 2 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "body"
    p[0] = create_node(p)


def p_stmt(p):
    '''stmt : expr SEMICOLON
            | defvar SEMICOLON
            | IF LPARANT expr RPARANT stmt
            | IF LPARANT expr RPARANT stmt ELSE stmt
            | WHILE LPARANT expr RPARANT DO stmt
            | FOREACH LPARANT ID OF expr RPARANT stmt
            | RETURN expr SEMICOLON
            | COLON body END'''
    print(f"rule 3 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "stmt"
    p[0] = create_node(p)


def p_defvar(p):
    '''defvar : VAL type ID'''
    print(f"rule 4 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "defva"
    p[0] = create_node(p)



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
    print(f"rule 5 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "expr"
    p[0] = create_node(p)


def p_flist(p):
    '''flist :
            | type ID
            | type ID COMMA flist'''
    print(f"rule 6 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "flist"
    p[0] = create_node(p)


def p_clist(p):
    '''clist :
            | expr
            | expr COMMA clist'''
    print(f"rule 7 reduced, line number: {p.lineno(1)}")
    
    #syntax tree
    p[0] = "clist"
    p[0] = create_node(p)


def p_type(p):
    '''type : INT
            | ARRAY
            | NIL'''
    print(f"rule 8 reduced, line number: {p.lineno(1)}")

    #syntax tree
    p[0] = "type"
    p[0] = create_node(p)

    #symbol tree




#def p_empty(p):
#    '''empty :'''
#    pass


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at token", p.type, p.lineno)
        # Just discard the token and tell the parser it's okay.
        #parser.errok()
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