
from hermit.lexer import lexer_run

class TestLext(object):
    def test_basic(self):
        r = lexer_run("12+12")
        assert [t.name for t in r] == ["T_NUMBER", "+", "T_NUMBER"]

    def test_float_addition(self):
        r = lexer_run("12.2+1.2")
        assert [t.name for t in r] == ['T_FLOAT_NUMBER', '+', 'T_FLOAT_NUMBER']
