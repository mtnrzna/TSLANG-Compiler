from anytree import NodeMixin, RenderTree
import uuid


class ASTNode(NodeMixin):  
    def __init__(self, name, id, children=None):
        self.name = name
        self.id = id
        if children:
            self.children = children

class ASTUtil(object):

    @staticmethod
    def prog_node1(func, prog):
        id = uuid.uuid4()
        children = [func]
        if prog:
            try:
                children.append(ASTUtil.prog_node(prog[1]["ast"], prog[2]["ast"]))
            except:
                children.append(ASTUtil.prog_node(prog[1]["ast"]))
        node = ASTNode("prgram", id, children)
        return node


class Node(object):
    def accept(self, visitor, table = None):
        return visitor.visit(self)
    def setParent(self, parent):
        self.parent = parent


class Prog1(Node):
    def __init__(self, func):
        self.func = func
        self.children = (func)

class Prog2(Node):
    def __init__(self, func, prog):
        self.func = func
        self.prog = prog
        self.children = (func, prog)

class Func1(Node):
    def __init__(self, iden , flist, type, body):
        self.iden = iden
        self.flist = flist
        self.type = type
        self.body = body
        self.children = (iden , flist, type, body)

class Body1(Node):
    def __init__(self, stmt):
        self.stmt = stmt
        self.children = (stmt)

class Body2(Node):
    def __init__(self, stmt, body):
        self.stmt = stmt
        self.body = body
        self.children = (stmt, body)

class Stmt1(Node):
    def __init__(self, expr):
        self.expr = expr
        self.children = (expr)

class Stmt2(Node):
    def __init__(self, defavr):
        self.defvar = defavr
        self.children = (defavr)

class Stmt3(Node):
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt
        self.children = (expr, stmt)

class Stmt4(Node):
    def __init__(self, expr, stmt, stmt2):
        self.expr = expr
        self.stmt = stmt
        self.stmt2 = stmt2
        self.children = (expr, stmt, stmt2)

class Stmt5(Node):
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt
        self.children = (expr, stmt)

class Stmt6(Node):
    def __init__(self, iden, expr, stmt):
        self.iden = iden
        self.expr = expr
        self.stmt = stmt
        self.children = (iden, expr, stmt)

class Stmt7(Node):
    def __init__(self, expr):
        self.expr = expr
        self.children = (expr)

class Stmt8(Node):
    def __init__(self, body):
        self.body = body
        self.children = (body)

class Defvar(Node):
    def __init__(self, type, iden):
        self.type = type
        self.iden = iden
        self.children = (type, iden)

class Expr1(Node):
    def __init__(self, iden, clist):
        self.iden = iden
        self.clist = clist
        self.children = (iden, clist)

class Expr2(Node):
    def __init__(self, expr, expr2):
        self.expr = expr
        self.expr2 = expr2
        self.children = (expr, expr2)

class Expr3(Node):
    def __init__(self, expr, expr2, expr3):
        self.expr = expr
        self.expr2 = expr2
        self.expr3 = expr3
        self.children = (expr, expr2, expr3)

class Expr4(Node):
    def __init__(self, expr, oper, expr2):
        self.expr = expr
        self.oper = oper
        self.expr2 = expr2
        self.children = (expr, oper, expr2)

class Expr5(Node):
    def __init__(self, oper, expr):
        self.oper = oper
        self.expr = expr
        self.children = (oper, expr)

class Expr6(Node):
    def __init__(self, expr):
        self.expr = expr
        self.children = (expr)

class Expr7(Node):
    def __init__(self, iden):
        self.iden = iden
        self.children = (iden)

class Expr8(Node):
    def __init__(self, num):
        self.num = num
        self.children = (num)

class Flist2(Node):
    def __init__(self, type, iden):
        self.type = type
        self.iden = iden
        self.children = (type, iden)

class Flist3(Node):
    def __init__(self, type, iden, flist):
        self.type = type
        self.iden = iden
        self.flist = flist
        self.children = (type, iden, flist)

class Clist2(Node):
    def __init__(self, expr):
        self.expr = expr
        self.children = (expr)

class Clist3(Node):
    def __init__(self, expr, clist):
        self.expr = expr
        self.clist = clist
        self.children = (clist)

class Type(Node):
    def __init__(self, type_value):
        self.type_value = type_value
        self.children = (type_value)

class Num(Node):
    def __init__(self, num_value):
        self.num_value = num_value
        self.children = (num_value)

class Iden(Node):
    def __init__(self, iden_value):
        self.iden_value = iden_value
        self.children = (iden_value)

class Empty(Node):
    def __init__(self):
        self.name = ""
        self.children = ()
