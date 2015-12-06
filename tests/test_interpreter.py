
from hermit.astcompiler import compile_ast
from hermit.sourceparser import parse
from hermit.interpreter import run_bytecode

class TestInterpreter(object):
    def interpret(self, source):
        bc = compile_ast('<input>', source, parse(source))
        frame = run_bytecode(bc)
        return frame.pop()

    def test_basic(self):
        self.interpret("12") == 12

    def test_addition(self):
        self.interpret("1+2") == 3

    def test_assignment(self):
        self.interpret("a=3") == 3

    def test_assignment_statement(self):
        self.interpret("a=3;a") == 3
