from hermit.sourceparser import parse
from hermit.astcompiler import compile_ast, bc_preprocess


class TestCompiler(object):
    def compare(self, bc, expected):
        expected = bc_preprocess(expected)
        bcdump = bc.dump()
        bcdump = bcdump.splitlines()
        expected = expected.splitlines()
        maxlen = max(len(expected), len(bcdump))
        expected += ['' * (maxlen - len(expected))]
        bcdump += ['' * (maxlen - len(bcdump))]
        print "Got:" + " " * 26 + "Expected:"
        for bcline, expline in zip(bcdump, expected):
            print "%s%s %s" % (bcline, " " * (30 - len(bcline)), expline)
            bcline = bcline.split()
            expline = expline.split()
            # we fail if the line we got is different than the expected line,
            # possibly after removing the first word (the index number)
            if bcline != expline and bcline[1:] != expline:
                assert False

    def check_compile(self, source, expected=None):
        ast = parse(source)
        bc = compile_ast('<input>', source, ast)
        if expected is not None:
            self.compare(bc, expected)
        return bc

    def test_basic(self):
        self.check_compile("12+13", """
        LOAD_CONST 0
        LOAD_CONST 1
        ADD
        """)

    def test_assignment(self):
        self.check_compile("a=3", """
        LOAD_CONST 0
        STORE_LOCAL 0
        """)
