# Everything is either an Atom or a Cons

class Error:
    # Lisp errors
    class UnmatchedParenthesesException(Exception): pass
    class UndefinedFunctionException(Exception): pass
    class UndefinedVariableException(Exception): pass


class Atom:
    # Non-cons object
    def __init__(self, val, line_num):
        self.val = val
        self._line_num = line_num  # For debugging


class Value(Atom):
    # Self-evaluating object e.x. int, float, str
    pass


class Symbol(Atom):
    # Represents the name of a binding in the env
    pass


class Cons:
    def __init__(self, car, cdr, preserved=False):
        self.car = car
        self.cdr = cdr
        self.preserved = preserved  # Structure should not be changed (see Lexer.ListBuilder.add)


class Environment:
    def __init__(self):
        self.bindings = {}

    def bind(self, symbol: Symbol, item):
        self.bindings[symbol.val] = item

    def copy(self):
        return self.bindings.copy()

    def __getitem__(self, item):
        return self.bindings[item]


class BuiltIns:
    pass


class Lexer:
    class ConsBuilder:
        def __init__(self):
            self.q = []

        def empty(self):
            return len(self.q) == 0

        def add(self, leaf):
            if len(self.q) == 0:  # Not in any list
                return False
            cons = self.q[-1]
            while True:
                if cons.car is None:  # (NIL . NIL)
                    # Should only be reached on 1st call immediately after `start_list`
                    cons.car = leaf
                    break
                elif cons.cdr is None:  # (x . NIL)
                    # Should only be reached on 2nd call immediately after `start_list`
                    cons.cdr = leaf
                    break
                else:  # (x . y)
                    #  The purpose of `Cons.__preserved`
                    #  (1 2 3 4)       vs.      (1 (2 3) 4)
                    #  (1 (2 (3 . 4)))      (1 ((2 . 3) 4))
                    #  Here, Cons(2 . 3).preserved is marked True in `close_list`
                    #  This preserves ((2 . 3) 4) instead of (2 (3 . 4))
                    if type(cons.cdr) is Cons and not cons.cdr.preserved:
                        cons = cons.cdr
                    else:
                        cons.cdr = Cons(car=cons.cdr, cdr=leaf)  # (x . (y . leaf))
                        break
            return True

        def start_list(self):
            self.q.append(Cons(car=None, cdr=None))

        def close_list(self):
            cons = self.q.pop()
            if len(self.q) == 0:
                return cons
            cons.preserved = True
            self.add(cons)

        def clear(self):
            self.q.clear()

    def __init__(self):
        self.cons_builder = self.ConsBuilder()
        self.result = []
        self.symbol_build = ''

    def lex(self, code: str) -> list:
        #  Returns list of Atoms/Cons to be evaluated
        self.cons_builder.clear()
        self.result.clear()
        lines = list(map(lambda l: l if ';' not in l else l[:l.index(';')], code.strip().split('\n')))
        for line_num, line in enumerate(lines):
            for char in line:
                if char == ' ':
                    self.exit_atom_build(line_num)
                elif char == '(':
                    self.exit_atom_build(line_num)
                    self.cons_builder.start_list()
                elif char == ')':
                    self.exit_atom_build(line_num)
                    try:
                        returned_list = self.cons_builder.close_list()
                    except IndexError:
                        raise Error.UnmatchedParenthesesException(line_num)
                    if returned_list is not None:
                        self.result.append(returned_list)
                else:
                    self.enter_atom_build(char)
        if not self.cons_builder.empty():
            raise Error.UnmatchedParenthesesException(len(lines) - 1)
        return self.result

    def enter_atom_build(self, char):
        self.symbol_build += char

    def exit_atom_build(self, line_num):
        if len(self.symbol_build) > 0:
            try:
                atom = Value(float(self.symbol_build), line_num)
            except ValueError:
                try:
                    atom = Value(int(self.symbol_build), line_num)
                except ValueError:
                    atom = Symbol(self.symbol_build, line_num)

            if not self.cons_builder.add(atom):
                self.result.append(atom)
            self.symbol_build = ''


class Evaluator:
    def evaluate(self, obj, env: Environment):
        if type(obj) is Atom:
            pass
        elif type(obj) is Cons:
            # (func . args)
            function = env[obj.car]
            arguments = obj.cdr
            self.call_function(function, arguments, env)

    def call_function(self, function, arguments, env):
        pass


x = Lexer().lex('(1 (2 3 4) 5)')
pass
