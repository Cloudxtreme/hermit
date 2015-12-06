from rpython.rlib.streamio import open_file_as_stream


import hermit
from hermit.sourceparser import parse
from hermit import bytecode as bc_consts
from hermit.astcompiler import compile_ast

from rlib.rreadline import readline


BANNER = "%s %s\n" % (hermit.__name__, hermit.__version__)
PS1 = ">>> "
PS2 = "... "


class Frame(object):
    def __init__(self, varnum):
        self.valuestack = []
        self.variables = [None] * varnum

    def push(self, v):
        self.valuestack.append(v)

    def peek(self):
        return self.valuestack[-1]

    def pop(self):
        return self.valuestack.pop()


class Interpreter(object):

    def __init__(self, debug=False, banner=BANNER, ps1=PS1, ps2=PS2):
        self.debug = debug
        self.banner = banner
        self.ps1 = ps1
        self.ps2 = ps2

    def runstring(self, s):
        ast = parse(s)

        bc = compile_ast("<input>", s, ast)
        if self.debug:  # pragma: no cover
            print bc.dump()

        return self.run(bc)

    def runfile(self, filename):
        f = open_file_as_stream(filename)
        s = f.readall()
        f.close()

        return self.runstring(s)

    def repl(self, banner=None, ps1=None, ps2=None):  # pragma: no cover
        banner = banner or self.banner
        ps1 = ps1 or self.ps1
        ps2 = ps2 or self.ps2

        print banner

        while True:
            try:
                s = readline(ps1).strip()
            except EOFError:
                break

            frame = self.runstring(s)
            result = frame.pop()
            if result is not None:
                print result

    def run(self, bytecode):
        frame = Frame(bytecode.varnum)
        code = bytecode.code
        i = 0
        while i < len(code):
            nextc = ord(code[i])
            if nextc == bc_consts.LOAD_CONST:
                i = self.load_const(i, frame, bytecode)
            elif nextc == bc_consts.ADD:
                i = self.add(i, frame, bytecode)
            elif nextc == bc_consts.STORE_LOCAL:
                i = self.store_local(i, frame, bytecode)
            elif nextc == bc_consts.LOAD_LOCAL:
                i = self.load_local(i, frame, bytecode)
            elif nextc == bc_consts.DISCARD_TOP:
                i = self.discard_top(i, frame, bytecode)
            else:
                raise Exception("Illegal bytecode %s" % nextc)
        return frame

    def add(self, pos, frame, bytecode):
        right = frame.pop()
        left = frame.pop()
        frame.push(left + right)
        return pos + 1

    def load_const(self, i, frame, bytecode):
        i, arg = bytecode.next_arg(i + 1)
        frame.push(bytecode.consts[arg])
        return i

    def store_local(self, i, frame, bytecode):
        i, arg = bytecode.next_arg(i + 1)
        value = frame.peek()
        frame.variables[arg] = value
        return i

    def discard_top(self, i, frame, bytecode):
        frame.pop()
        return i + 1

    def load_local(self, i, frame, bytecode):
        i, arg = bytecode.next_arg(i + 1)
        frame.push(frame.variables[arg])
        return i


def run_bytecode(bc):
    return Interpreter().run(bc)
