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
    def __init__(self, func, lineno):
        self.lineno = lineno
        self.func = func
        self.children = (func,)

class Prog2(Node):
    def __init__(self, func, prog, lineno):
        self.lineno = lineno
        self.func = func
        self.prog = prog
        self.children = (func, prog,)

class Func(Node):
    def __init__(self, iden , flist, type, body, lineno):
        self.lineno = lineno
        self.iden = iden
        self.flist = flist
        self.type = type
        self.body = body
        self.children = (iden , flist, type, body,)

class Body1(Node):
    def __init__(self, stmt, lineno):
        self.lineno = lineno
        self.stmt = stmt
        self.children = (stmt,)

class Body2(Node):
    def __init__(self, stmt, body, lineno):
        self.lineno = lineno
        self.stmt = stmt
        self.body = body
        self.children = (stmt, body,)

class Stmt1(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

class Stmt2(Node):
    def __init__(self, defavr, lineno):
        self.lineno = lineno
        self.defvar = defavr
        self.children = (defavr,)

class Stmt3(Node):
    def __init__(self, expr, stmt, lineno):
        self.lineno = lineno
        self.expr = expr
        self.stmt = stmt
        self.children = (expr, stmt,)

class Stmt4(Node):
    def __init__(self, expr, stmt, stmt2, lineno):
        self.lineno = lineno
        self.expr = expr
        self.stmt = stmt
        self.stmt2 = stmt2
        self.children = (expr, stmt, stmt2,)

class Stmt5(Node):
    def __init__(self, expr, stmt, lineno):
        self.lineno = lineno
        self.expr = expr
        self.stmt = stmt
        self.children = (expr, stmt,)

class Stmt6(Node):
    def __init__(self, iden, expr, stmt, lineno):
        self.lineno = lineno
        self.iden = iden
        self.expr = expr
        self.stmt = stmt
        self.children = (iden, expr, stmt,)

class Stmt7(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

class Stmt8(Node):
    def __init__(self, body, lineno):
        self.lineno = lineno
        self.body = body
        self.children = (body,)

class Defvar(Node):
    def __init__(self, type, iden, lineno):
        self.lineno = lineno
        self.type = type
        self.iden = iden
        self.children = (type, iden,)

class Expr1(Node):
    def __init__(self, iden, clist, lineno):
        self.lineno = lineno
        self.iden = iden
        self.clist = clist
        self.children = (iden, clist,)

class Expr2(Node):
    def __init__(self, expr, expr2, lineno):
        self.lineno = lineno
        self.expr = expr
        self.expr2 = expr2
        self.children = (expr, expr2,)

class Expr3(Node):
    def __init__(self, expr, expr2, expr3, lineno):
        self.lineno = lineno
        self.expr = expr
        self.expr2 = expr2
        self.expr3 = expr3
        self.children = (expr, expr2, expr3,)

class Expr4(Node):
    def __init__(self, expr, oper, expr2, lineno):
        self.lineno = lineno
        self.expr = expr
        self.oper = oper
        self.expr2 = expr2
        self.children = (expr, oper, expr2,)

class Expr5(Node):
    def __init__(self, oper, expr, lineno):
        self.lineno = lineno
        self.oper = oper
        self.expr = expr
        self.children = (oper, expr,)

class Expr6(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

class Expr7(Node):
    def __init__(self, iden, lineno):
        self.lineno = lineno
        self.iden = iden
        self.children = (iden,)

class Expr8(Node):
    def __init__(self, num, lineno):
        self.lineno = lineno
        self.num = num
        self.children = (num,)

class Flist2(Node):
    def __init__(self, type, iden, lineno):
        self.lineno = lineno
        self.type = type
        self.iden = iden
        self.children = (type, iden,)

class Flist3(Node):
    def __init__(self, type, iden, flist, lineno):
        self.lineno = lineno
        self.type = type
        self.iden = iden
        self.flist = flist
        self.children = (type, iden, flist,)

class Clist2(Node):
    def __init__(self, expr, lineno):
        self.lineno = lineno
        self.expr = expr
        self.children = (expr,)

class Clist3(Node):
    def __init__(self, expr, clist, lineno):
        self.lineno = lineno
        self.expr = expr
        self.clist = clist
        self.children = (expr, clist,)

class Type(Node):
    def __init__(self, type_value, lineno):
        self.lineno = lineno
        self.type_value = type_value
        self.children = (type_value,)

class Num(Node):
    def __init__(self, num_value, lineno):
        self.lineno = lineno
        self.num_value = num_value
        self.children = (num_value,)

class Iden(Node):
    def __init__(self, iden_value, lineno):
        self.lineno = lineno
        self.iden_value = iden_value
        self.children = (iden_value,)

class Empty(Node):
    def __init__(self, lineno):
        self.lineno = lineno
        self.name = ""
        self.children = ()
