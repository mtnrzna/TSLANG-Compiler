from compiler_levels.lexer.tokens import Tokens
import config
from utils.syntax_tree import SyntaxTreeUtil
from utils.AST import *
from compiler_levels.lexer.tokens import Tokens
from utils.symbol_table import SymbolTable

class Grammar(object):
    
    tokens = Tokens.tokens
        
    errors = 0
   
    #  prog rules
    def p_prog1(p):
        '''prog : func'''
        p[0] = "prog"
        p[0] = {
            "name":"prog",
            "st": SyntaxTreeUtil.create_node(p), # st: syntax tree
            "ast" : Prog1(p[1]["ast"]) # ast: abstract syntax tree
        }
        config.syntax_tree = p[0]["st"]



    def p_prog2(p):
        '''prog : func prog'''
        p[0] = "prog"
        p[0] = {
            "name":"prog",
            "st": SyntaxTreeUtil.create_node(p), # st: syntax tree
            "ast" : Prog2(p[1]["ast"], p[2]["ast"]) # ast: abstract syntax tree
        }
        config.syntax_tree = p[0]["st"]


   
    #  func rules
    def p_func1(p):
        '''func : FUNCTION iden LPARANT flist RPARANT RETURNS type COLON body END'''
        p[0] = "func"
        p[0] = {
            "name":"func",
            "st": SyntaxTreeUtil.create_node(p),
            "ast" : Func1(p[2]["ast"], p[4]["ast"], p[7]["ast"], p[9]["ast"])
        }

    def p_func1_error(p): # For errors in the paranthesis
        '''func : FUNCTION iden LPARANT error RPARANT RETURNS type COLON body END'''
        print(f"{p[4].lineno}: Error corrected. The syntax is 'function iden ( flist ) returns type: body end'")
        p[4] = p[4].value
        p[0] = "func"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast" : Func1(p[2]["ast"], p[4], p[7]["ast"], p[9]["ast"])
        }


    def p_func2(p):
        '''func : empty'''
        p[0] = "func"
        p[0] = {
            "name":"func",
            "st": SyntaxTreeUtil.create_node(p),
            "ast" : Empty()
        }
        


    def p_body1(p):
        '''body : stmt'''
        p[0] = "body"
        p[0] = {
            "name":"body",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Body1(p[1]["ast"])
        }

    
    def p_body2(p):
        '''body : stmt body'''
        p[0] = "body"
        p[0] = {
            "name":"body",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Body2(p[1]["ast"], p[2]["ast"])
        }

   
    #  stmt rules
    def p_stmt1(p):
        '''stmt : expr SEMICOLON'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt1(p[1]["ast"])
        }


    def p_stmt2(p):
        '''stmt : defvar SEMICOLON'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt2(p[1]["ast"])
        }


    def p_stmt3(p):
        '''stmt : IF LPARANT expr RPARANT stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt3(p[3]["ast"], p[5]["ast"])
        }


    def p_stmt3_error(p): # For errors in the paranthesis
        '''stmt : IF LPARANT error RPARANT stmt'''
        print(f"{p[3].lineno}: Error corrected. The syntax is 'if ( clist ) stmt'")
        p[3] = p[3].value
        p[0] = "stmt"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt3(p[3], p[5]["ast"])
        }

    def p_stmt4(p):
        '''stmt : IF LPARANT expr RPARANT stmt ELSE stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt4(p[3]["ast"], p[5]["ast"], p[7]["ast"])
        }


    def p_stmt4_error(p): # For errors in the paranthesis
        '''stmt : IF LPARANT error RPARANT stmt ELSE stmt'''
        print(f"{p[3].lineno}: Error corrected. The syntax is 'if ( clist ) stmt else stmt'")
        p[3] = p[3].value
        p[0] = "stmt"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt4(p[3], p[5]["ast"], p[7]["ast"])
        }

    def p_stmt5(p):
        '''stmt : WHILE LPARANT expr RPARANT DO stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Stmt5(p[3]["ast"], p[6]["ast"])
        }


    def p_stmt5_error(p): # For errors in the paranthesis
        '''stmt : WHILE LPARANT error RPARANT DO stmt'''
        print(f"{p[3].lineno}: Error corrected. The syntax is 'while ( expr ) do stmt'")
        p[3] = p[3].value
        p[0] = "stmt"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt5(p[3], p[6]["ast"])
        }


    def p_stmt6(p):
        '''stmt : FOREACH LPARANT iden OF expr RPARANT stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Stmt6(p[3]["ast"], p[5]["ast"], p[7]["ast"])
        }

    
    def p_stmt7(p):
        '''stmt : RETURN expr SEMICOLON'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt7(p[2]["ast"])
        }


    def p_stmt8(p):
        '''stmt : COLON body END'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt8(p[2]["ast"])
        }


   
    #  devfvar rules
    def p_defvar(p):
        '''defvar : VAL type iden'''
        p[0] = "defvar"
        p[0] = {
            "name":"defvar",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Defvar(p[2]["ast"], p[3]["ast"])
        }


   
    #  expr rules
    def p_expr1(p):
        '''expr : iden LPARANT clist RPARANT'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr1(p[1]["ast"], p[3]["ast"])
        }


    def p_expr1_error(p): # For errors in the paranthesis
        '''expr : iden LPARANT error RPARANT'''
        print(f"{p[3].lineno}: Error corrected. The syntax is 'iden ( clist )'")
        p[3] = p[3].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr1(p[1]["ast"], p[3])
        }

    def p_expr2(p):
        '''expr : expr LBRACKET expr RBRACKET'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr2(p[1]["ast"], p[3]["ast"])
        }


    def p_expr2_error(p): # For errors in the brackets
        '''expr : expr LBRACKET error RBRACKET'''
        print(f"{p[3].lineno}: Error corrected. The syntax is 'expr [ expr ]'")
        p[3] = p[3].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr1(p[1]["ast"], p[3])
        }


    def p_expr3(p):
        '''expr : expr QUEST_MARK expr COLON expr'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr3(p[1]["ast"], p[3]["ast"], p[5]["ast"])
        }


    def p_expr3_error(p): # For errors when you put "";" instead of ":"
        '''expr : expr QUEST_MARK expr error expr'''
        print(f"{p[4].lineno}: Error corrected. The syntax is 'expr ? expr : expr'")
        p[4] = p[4].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr3(p[1]["ast"], p[3]["ast"], p[5]["ast"])
        }


    def p_expr4(p):
        '''expr : expr EQUAL expr
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
                | expr AMP_AMP expr'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr4(p[1]["ast"], p[2], p[3]["ast"])
        }


    def p_expr5(p):
        '''expr : EXCL_MARK expr
                | MINUS expr
                | PLUS expr'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr5(p[1], p[2]["ast"])
        }


    def p_expr6(p):
        '''expr : LPARANT expr RPARANT'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr6(p[2]["ast"])
        }

    def p_expr6_error(p):
        '''expr : LPARANT error RPARANT'''
        print(f"{p[2].lineno}: Error corrected. The syntax is '( expr )'")
        p[2] = p[2].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr6(p[2])
        }


    def p_expr7(p):
        '''expr : iden'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr7(p[1]["ast"])
        }


    def p_expr8(p):
        '''expr : num'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr8(p[1]["ast"])
        }

    
   
    #  flist rules
    def p_flist1(p):
        '''flist : empty'''
        p[0] = "flist"
        p[0] = {
            "name":"flist",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Empty()
        }


    def p_flist2(p):
        '''flist : type iden'''
        p[0] = "flist"
        p[0] = {
            "name":"flist",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist2(p[1]["ast"], p[2]["ast"])
        }


    def p_flist3(p):
        '''flist : type iden COMMA flist'''
        p[0] = "flist"
        p[0] = {
            "name":"flist",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist3(p[1]["ast"], p[2]["ast"], p[4]["ast"])
        }



    # clist rules
    def p_clist1(p):
        '''clist : empty'''
        p[0] = "clist"
        p[0] = {
            "name":"clist",
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Empty()
        }


    def p_clist2(p):
        '''clist : expr'''
        p[0] = "clist"
        p[0] = {
            "name":"clist",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Clist2(p[1]["ast"])
        }


    def p_clist3(p):
        '''clist : expr COMMA clist'''
        p[0] = "clist"
        p[0] = {
            "name":"clist",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Clist3(p[1]["ast"], p[3]["ast"])
        }

    

    # type rule
    def p_type(p):
        '''type : INT
                | ARRAY
                | NIL'''
        p[0] = "type"
        p[0] = {
            "name":"type",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Type(p[1])
        }



    # type rule
    def p_num(p):
        '''num : NUMBER'''
        p[0] = "number"
        p[0] = {
            "name":"number",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Num(p[1])
        }



    # iden rule
    def p_iden(p):
        '''iden : ID'''
        p[0] = "iden"
        p[0] = {
            "name":"iden",
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Iden(p[1])
        }




    def p_empty(p):
        '''empty :'''
        pass


    # Error rule for syntax errors
    def p_error(p):
        if p:
            print(f"{p.lineno}: Syntax error at token: {p.value} ")
            Grammar.errors += 1
            # Just discard the token and tell the parser it's okay.
            #parser.errok()
        else:
            print("Syntax error at EOF")

    #Set up precedence
    precedence = (
        ('left', 'error'),
        ('left', 'AMP_AMP', 'EXCL_MARK', 'PIPE_PIPE', 'SMALL_EQUAL', 'BIG_EQUAL', 'EXCL_EQUAL', 'EQUAL_EQUAL', 'SMALL', 'BIG'),
        ('left', 'EQUAL', 'QUEST_MARK', 'COLON'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'PERCENT'),
        ('left', 'LPARANT', 'RPARANT', 'LBRACKET', 'RBRACKET')
    )