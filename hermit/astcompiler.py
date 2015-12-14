from hermit.sourceparser import BinaryOp, ConstInt, Assignment, SemicolonExpr,\
     Variable
from hermit import bytecode


class CompilerContext(object):
    def __init__(self):
        self.data = []
        self.consts = []
        self.varnums = {}

    def register_var(self, v):
        try:
            return self.varnums[v]
        except KeyError:
            r = len(self.varnums)
            self.varnums[v] = r
            return r

    def register_int_const(self, intval):
        self.consts.append(intval)
        return len(self.consts) - 1

    def emit(self, bc, arg=-42):
        self.data.append(chr(bc))
        if bc >= bytecode.BYTECODE_HAS_ARG:
            assert arg >= 0
            a = arg
            while a >= 0x80:
                self.data.append(chr((a & 0x7f) | 0x80))
                a ^= 0x80
                a >>= 7
            self.data.append(chr(a))
        else:
            assert arg == -42

    def build(self, name):
        return bytecode.Bytecode("".join(self.data), name, self.consts,
                                 len(self.varnums))


class __extend__(BinaryOp):
    def compile(self, ctx):
        self.left.compile(ctx)
        self.right.compile(ctx)
        ctx.emit(bytecode.BIN_OP_TO_BC[self.oper])


class __extend__(ConstInt):
    def compile(self, ctx):
        arg = ctx.register_int_const(self.intval)
        ctx.emit(bytecode.LOAD_CONST, arg)


class __extend__(Assignment):
    def compile(self, ctx):
        self.node.compile(ctx)
        arg = ctx.register_var(self.varname)
        ctx.emit(bytecode.STORE_LOCAL, arg)


class __extend__(SemicolonExpr):
    def compile(self, ctx):
        self.left.compile(ctx)
        ctx.emit(bytecode.DISCARD_TOP)
        self.right.compile(ctx)


class __extend__(Variable):
    def compile(self, ctx):
        ctx.emit(bytecode.LOAD_LOCAL, ctx.register_var(self.name))


def compile_ast(name, source, ast):
    ctx = CompilerContext()
    ast.compile(ctx)
    return ctx.build(name)


def bc_preprocess(source):
    l = []
    for i in source.splitlines():
        if '#' in i:
            i = i[:i.find('#')]
        i = i.strip()
        if not i:
            continue
        l.append(i)
    return "\n".join(l)
