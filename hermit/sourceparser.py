from rply import ParserGenerator
from hermit.lexer import RULES, Lexer
from rpython.tool.pairtype import extendabletype

PRECEDENCES = [("left", [";"]), ("left", ["="]), ("left", ["+"]), ]


class Node(object):
    """ Base class for all ast nodes
    """

    __metaclass__ = extendabletype

    # so we can do class __extend__ in astcompiler.py

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __repr__(self):
        values = sorted(self.__dict__.items())
        dictrepr = " ".join([("%s=%r" % (k, v)) for k, v in values])
        return "%s(%s)" % (self.__class__.__name__, dictrepr)


class BinaryOp(Node):
    """ Binary operation (like +)
    """

    def __init__(self, oper, left, right):
        self.oper = oper
        self.left = left
        self.right = right


class ConstInt(Node):
    """ Constant integer in the code
    """

    def __init__(self, intval):
        self.intval = intval


class ConstFloat(Node):
    """ Constant float in the code
    """

    def __init__(self, floatval):
        self.floatval = floatval


class Assignment(Node):
    def __init__(self, varname, node):
        self.varname = varname
        self.node = node


class SemicolonExpr(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Variable(Node):
    def __init__(self, name):
        self.name = name


class SourceParser(object):
    """ Parse a given input using a lexer
    """

    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        return self.parser.parse(self.lexer, state=self)

    pg = ParserGenerator([d for _, d in RULES],
                         cache_id='hermit',
                         precedence=PRECEDENCES)

    @pg.production('main : expr')
    def main_expr(self, p):
        return p[0]

    @pg.production('expr : expr + expr')
    def expr_plus(self, p):
        return BinaryOp("+", p[0], p[2])

    @pg.production('expr : T_NUMBER')
    def expr_number(self, p):
        return ConstInt(int(p[0].getstr()))

    @pg.production('expr : T_FLOAT_NUMBER')
    def expr_float_number(self, p):
        return ConstFloat(float(p[0].getstr()))

    @pg.production('expr : T_VARIABLE = expr')
    def expr_variable_assign(self, p):
        return Assignment(p[0].getstr(), p[2])

    @pg.production('expr : expr ; expr')
    def expr_semicolon(self, p):
        return SemicolonExpr(p[0], p[2])

    @pg.production('expr : T_VARIABLE')
    def expr_variable(self, p):
        return Variable(p[0].getstr())

    parser = pg.build()


def parse(source):
    parser = SourceParser(Lexer().input(source, 0))
    return parser.parse()
