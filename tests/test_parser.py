
from hermit.sourceparser import parse, BinaryOp, ConstInt, ConstFloat,\
     Assignment, SemicolonExpr, Variable

class TestParser(object):
    def test_basic(self):
        assert parse("12+1") == BinaryOp("+", ConstInt(12), ConstInt(1))

    def test_repr(self):
        exp = ("BinaryOp(left=ConstInt(intval=12) oper='+' right="
               "ConstInt(intval=1))")
        assert repr(BinaryOp("+", ConstInt(12), ConstInt(1))) == exp

    def test_parse_floats(self):
        assert parse("1.2+1") == BinaryOp("+", ConstFloat(1.2),
                                          ConstInt(1))

    def test_variable_assignment(self):
        assert parse("a=3") == Assignment("a", ConstInt(3))

    def test_statements(self):
        assert parse("a=3;a") == SemicolonExpr(Assignment("a", ConstInt(3)),
                                               Variable("a"))
