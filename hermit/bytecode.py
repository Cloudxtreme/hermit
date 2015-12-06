
from rpython.rlib.unroll import unrolling_iterable

# name, num_args, effect on stack
BYTECODES = [
    ('LOAD_CONST', 1, +1),
    ('ADD', 0, +1),
    ('STORE_LOCAL', 1, 0),
    ('DISCARD_TOP', 0, -1),
    ('LOAD_LOCAL', 1, +1),
]

assert len(BYTECODES) < 256
BYTECODES.sort(key=lambda t: t[1])   # first the no-arg, then the one-arg

BYTECODE_HAS_ARG = 0
while BYTECODES[BYTECODE_HAS_ARG][1] == 0:
    BYTECODE_HAS_ARG += 1
BYTECODE_NAMES = []
BYTECODE_STACK_EFFECTS = []

def _setup():
    for i, (bc, numargs, stack_effect) in enumerate(BYTECODES):
        globals()[bc] = i
        assert numargs == (i >= BYTECODE_HAS_ARG)
        BYTECODE_NAMES.append(bc)
        BYTECODE_STACK_EFFECTS.append(stack_effect)
_setup()

BIN_OP_TO_BC = {'+': ADD}

class IllegalInstruction(Exception):
    pass

if __name__ == '__main__':
    for i, (bc, _, _) in enumerate(BYTECODES):
        print i, bc

unroll_k = unrolling_iterable([7, 14, 21, 28])

class Bytecode(object):
    def __init__(self, code, name, consts, varnum):
        self.code = code
        self.name = name
        self.consts = consts
        self.varnum = varnum

    def next_arg(self, i):
        a = ord(self.code[i])
        i += 1
        if a >= 0x80:
            for k in unroll_k:
                b = ord(self.code[i])
                i += 1
                a ^= (b << k)
                if b < 0x80:
                    break
            else:
                raise IllegalInstruction("error")
        return i, a

    def dump(self):
        i = 0
        lines = []
        while i < len(self.code):
            #if i == self._marker:   # not translated
            #    line = ' ===> '
            #else:
            line = '%4d  ' % (i,)
            c = ord(self.code[i])
            line += BYTECODE_NAMES[c]
            i += 1
            if c >= BYTECODE_HAS_ARG:
                i, arg = self.next_arg(i)
                line += " %s" % arg
            lines.append(line)
        return "\n".join(lines)
