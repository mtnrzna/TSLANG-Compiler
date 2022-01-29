from compiler_levels.lexer.tokens import Tokens
import config
from utils.syntax_tree import SyntaxTreeUtil
from utils.AST import *

class Grammar(object):
    
    tokens = Tokens.tokens
        

    def __init__(self, parser_errors):
        self.parser_errors = parser_errors


    #  prog rules
    def p_prog1(self, p):
        '''prog : func'''
        p[0] = "prog"
        p[0] = {
            "name":"prog",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), # st: syntax tree
            "ast" : Prog1(p[1]["ast"], self.lexer.lineno) # ast: abstract syntax tre, self.lexer.linenoe
        }
        config.syntax_tree = p[0]["st"]
        config.ast = p[0]["ast"]
        

    def p_prog2(self, p):
        '''prog : func prog'''
        p[0] = "prog"
        p[0] = {
            "name":"prog",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), # st: syntax tree
            "ast" : Prog2(p[1]["ast"], p[2]["ast"], self.lexer.lineno) # ast: abstract syntax tre, self.lexer.linenoe
        }
        config.syntax_tree = p[0]["st"]
        config.ast = p[0]["ast"]



   
    #  func rules
    def p_func(self, p):
        '''func : FUNCTION iden LPARANT flist RPARANT RETURNS type COLON body END'''
        p[0] = "func"
        p[0] = {
            "name":"func",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast" : Func(p[2]["ast"], p[4]["ast"], p[7]["ast"], p[9]["ast"], self.lexer.lineno)
        }

    def p_func_error(self, p): # For errors in the paranthesis
        '''func : FUNCTION iden LPARANT error RPARANT RETURNS type COLON body END'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is 'function iden ( flist ) returns type: body end'","lineno": p.lineno})
        p[4] = p[4].value
        p[0] = "func"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast" : Func(p[2]["ast"], p[4], p[7]["ast"], p[9]["ast"], self.lexer.lineno)
        }


    def p_body1(self, p):
        '''body : stmt'''
        p[0] = "body"
        p[0] = {
            "name":"body",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Body1(p[1]["ast"], self.lexer.lineno)
        }

    
    def p_body2(self, p):
        '''body : stmt body'''
        p[0] = "body"
        p[0] = {
            "name":"body",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Body2(p[1]["ast"], p[2]["ast"], self.lexer.lineno)
        }

   
    #  stmt rules
    def p_stmt1(self, p):
        '''stmt : expr SEMICOLON'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt1(p[1]["ast"], self.lexer.lineno)
        }


    def p_stmt2(self, p):
        '''stmt : defvar SEMICOLON'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt2(p[1]["ast"], self.lexer.lineno)
        }


    def p_stmt3(self, p):
        '''stmt : IF LPARANT expr RPARANT stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt3(p[3]["ast"], p[5]["ast"], self.lexer.lineno)
        }


    def p_stmt3_error(self, p): # For errors in the paranthesis
        '''stmt : IF LPARANT error RPARANT stmt'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is 'if ( clist ) stmt'","lineno": p.lineno})
        p[3] = p[3].value
        p[0] = "stmt"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt3(p[3], p[5]["ast"], self.lexer.lineno)
        }

    def p_stmt4(self, p):
        '''stmt : IF LPARANT expr RPARANT stmt ELSE stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt4(p[3]["ast"], p[5]["ast"], p[7]["ast"], self.lexer.lineno)
        }


    def p_stmt4_error(self, p): # For errors in the paranthesis
        '''stmt : IF LPARANT error RPARANT stmt ELSE stmt'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is 'if ( clist ) stmt else stmt'","lineno": p.lineno})
        p[3] = p[3].value
        p[0] = "stmt"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt4(p[3], p[5]["ast"], p[7]["ast"], self.lexer.lineno)
        }

    def p_stmt5(self, p):
        '''stmt : WHILE LPARANT expr RPARANT DO stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Stmt5(p[3]["ast"], p[6]["ast"], self.lexer.lineno)
        }


    def p_stmt5_error(self, p): # For errors in the paranthesis
        '''stmt : WHILE LPARANT error RPARANT DO stmt'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is 'while ( expr ) do stmt'","lineno": p.lineno})
        p[3] = p[3].value
        p[0] = "stmt"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt5(p[3], p[6]["ast"], self.lexer.lineno)
        }


    def p_stmt6(self, p):
        '''stmt : FOREACH LPARANT iden OF expr RPARANT stmt'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Stmt6(p[3]["ast"], p[5]["ast"], p[7]["ast"], self.lexer.lineno)
        }

    
    def p_stmt7(self, p):
        '''stmt : RETURN expr SEMICOLON'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt7(p[2]["ast"], self.lexer.lineno)
        }


    def p_stmt8(self, p):
        '''stmt : COLON body END'''
        p[0] = "stmt"
        p[0] = {
            "name":"stmt",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Stmt8(p[2]["ast"], self.lexer.lineno)
        }


   
    #  devfvar rules
    def p_defvar(self, p):
        '''defvar : VAL type iden'''
        p[0] = "defvar"
        p[0] = {
            "name":"defvar",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Defvar(p[2]["ast"], p[3]["ast"], self.lexer.lineno)
        }


   
    #  expr rules
    def p_expr1(self, p):
        '''expr : iden LPARANT clist RPARANT'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr1(p[1]["ast"], p[3]["ast"], self.lexer.lineno)
        }


    def p_expr1_error(self, p): # For errors in the paranthesis
        '''expr : iden LPARANT error RPARANT'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is 'iden ( clist )'","lineno": p.lineno})
        p[3] = p[3].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr1(p[1]["ast"], p[3], self.lexer.lineno)
        }

    def p_expr2(self, p):
        '''expr : expr LBRACKET expr RBRACKET'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr2(p[1]["ast"], p[3]["ast"], self.lexer.lineno)
        }


    def p_expr2_error(self, p): # For errors in the brackets
        '''expr : expr LBRACKET error RBRACKET'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is 'expr [ expr ]'","lineno": p.lineno})
        p[3] = p[3].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr1(p[1]["ast"], p[3], self.lexer.lineno)
        }


    def p_expr3(self, p):
        '''expr : expr QUEST_MARK expr COLON expr'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr3(p[1]["ast"], p[3]["ast"], p[5]["ast"], self.lexer.lineno)
        }


    def p_expr3_error(self, p): # For errors when you put "";" instead of ":"
        '''expr : expr QUEST_MARK expr error expr'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is 'expr ? expr : expr'","lineno": p.lineno})
        p[4] = p[4].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr3(p[1]["ast"], p[3]["ast"], p[5]["ast"], self.lexer.lineno)
        }


    def p_expr4(self, p):
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
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr4(p[1]["ast"], p[2], p[3]["ast"], self.lexer.lineno)
        }


    def p_expr5(self, p):
        '''expr : EXCL_MARK expr
                | MINUS expr
                | PLUS expr'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr5(p[1], p[2]["ast"], self.lexer.lineno)
        }


    def p_expr6(self, p):
        '''expr : LPARANT expr RPARANT'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr6(p[2]["ast"], self.lexer.lineno)
        }

    def p_expr6_error(self, p):
        '''expr : LPARANT error RPARANT'''
        self.parser_errors.add_error({"message": "Error corrected. The syntax is '( expr )'","lineno": p.lineno})
        p[2] = p[2].value
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr6(p[2], self.lexer.lineno)
        }


    def p_expr7(self, p):
        '''expr : iden'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Expr7(p[1]["ast"], self.lexer.lineno)
        }


    def p_expr8(self, p):
        '''expr : num'''
        p[0] = "expr"
        p[0] = {
            "name":"expr",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Expr8(p[1]["ast"], self.lexer.lineno)
        }

    
   
    #  flist rules
    def p_flist1(self, p):
        '''flist : empty'''
        p[0] = "flist"
        p[0] = {
            "name":"flist",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Empty(self.lexer.lineno)
        }


    def p_flist2(self, p):
        '''flist : type iden'''
        p[0] = "flist"
        p[0] = {
            "name":"flist",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist2(p[1]["ast"], p[2]["ast"], self.lexer.lineno)
        }


    def p_flist3(self, p):
        '''flist : type iden COMMA flist'''
        p[0] = "flist"
        p[0] = {
            "name":"flist",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Flist3(p[1]["ast"], p[2]["ast"], p[4]["ast"], self.lexer.lineno)
        }



    # clist rules
    def p_clist1(self, p):
        '''clist : empty'''
        p[0] = "clist"
        p[0] = {
            "name":"clist",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p), 
            "ast": Empty(self.lexer.lineno)
        }


    def p_clist2(self, p):
        '''clist : expr'''
        p[0] = "clist"
        p[0] = {
            "name":"clist",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Clist2(p[1]["ast"], self.lexer.lineno)
        }


    def p_clist3(self, p):
        '''clist : expr COMMA clist'''
        p[0] = "clist"
        p[0] = {
            "name":"clist",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Clist3(p[1]["ast"], p[3]["ast"], self.lexer.lineno)
        }

    

    # type rule
    def p_type(self, p):
        '''type : INT
                | ARRAY
                | NIL'''
        p[0] = "type"
        p[0] = {
            "name":"type",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Type(p[1], self.lexer.lineno)
        }



    # type rule
    def p_num(self, p):
        '''num : NUMBER'''
        p[0] = "number"
        p[0] = {
            "name":"number",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Num(p[1], self.lexer.lineno)
        }



    # iden rule
    def p_iden(self, p):
        '''iden : ID'''
        p[0] = "iden"
        p[0] = {
            "name":"iden",
            "lineno": self.lexer.lineno,
            "st": SyntaxTreeUtil.create_node(p),
            "ast": Iden(p[1], self.lexer.lineno)
        }
        #print(f'token: \'{p[0]["name"]}\' at line: {p[0]["lineno"]}')





    def p_empty(self, p):
        '''empty :'''
        pass


    # Error rule for syntax errors
    def p_error(self, p):
        if p:
            self.parser_errors.add_error({"message": f"{p.lineno}: Syntax error at token: {p.value}","lineno": p.lineno})
            self.parser_errors.errors += 1
            # Just discard the token and tell the parser it's okay.
            #parser.errok()
        else:
            self.parser_errors.add_error({"message": "Syntax error at EOF", "lineno": None})
    #Set up precedence
    precedence = (
        ('left', 'error'),
        ('left', 'AMP_AMP', 'EXCL_MARK', 'PIPE_PIPE', 'SMALL_EQUAL', 'BIG_EQUAL', 'EXCL_EQUAL', 'EQUAL_EQUAL', 'SMALL', 'BIG'),
        ('left', 'EQUAL', 'QUEST_MARK', 'COLON'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'PERCENT'),
        ('left', 'LPARANT', 'RPARANT', 'LBRACKET', 'RBRACKET')
    )