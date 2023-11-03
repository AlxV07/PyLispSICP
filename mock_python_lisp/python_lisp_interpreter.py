# http://www.lispworks.com/documentation/lw50/CLHS/Body/03_aba.htm
# 3.1.2.1 Form Evaluation
# Forms fall into three categories: symbols, conses, and self-evaluating objects.

# Symbol & self-evaluating object forms are non-cons objects, or atoms.
# Self-evaluating objects are set values such as numbers and strings.
# Symbols are either variables or symbol macros (expands to function).

# A cons used as a form is called a compound form.
# If the car of the form a symbol, it is the name of a function form or a macro form to expand to.
# Otherwise, the car of the form is a lambda expression and the compound form is a lambda form.

class Error:
    # Lisp errors
    class UnmatchedParenthesesException(Exception): pass
    class UndefinedFunctionException(Exception): pass
    class UndefinedVariableException(Exception): pass


class Atom:
    # Non-cons object
    def __init__(self, val, line_num):
        self.val = val
        self._line_num = line_num  # For error printing


class Value(Atom):
    # Self-evaluating object e.x. int, float, str
    pass


class Number: pass


class String: pass


class Symbol(Atom):
    # Represents name of a binding in the environment
    pass


class Function: pass


class Cons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr


class Environment:
    def __init__(self, var_bindings=None, func_bindings=None):
        if var_bindings is None:
            var_bindings = dict()
        if func_bindings is None:
            func_bindings = dict()
        self.var_bindings = var_bindings
        self.func_bindings = func_bindings

    def bind_var(self, symbol: Symbol, item):
        self.var_bindings[symbol.val] = item

    def bind_func(self, symbol: Symbol, item):
        self.func_bindings[symbol.val] = item

    def get_var(self, symbol: Symbol):
        return self.var_bindings[symbol.val]

    def get_func(self, symbol: Symbol):
        return self.func_bindings[symbol.val]

    def copy(self):
        return self.var_bindings.copy(), self.func_bindings.copy()


class BuiltIns:
    global_vars = {
        "#'+": None,
        "#'-": None,
        "#'*": None,
        "#'/": None,

        "nil": None,
        "t": None,
    }

    global_funcs = {
        "cons": None,
        "car": None,
        "cdr": None,
        "list": None,

        "lambda": None,
        "defvar": None,
        "defun": None,
        "funcall": None,

        "if": None,
        "cond": None,

        "print": None,
    }


class Lexer:
    class ConsBuilder:
        def __init__(self):
            """
            root & tar cons for easy bookkeeping: what to return and what to add to, respectively

            ToBeConsed: (1 2 3 4)
            Root          | Target
            (1 2)            (1 2)
            (1 (2 3))        (2 3)
            (1 (2 (3 4)))    (3 4)

            ToBeConsed: (1 (2 3) 4)
            Root           | Target
            (1 None)       (1 None)
            (2 3)             (2 3)
            (1 (2 3))     (1 (2 3))
            (1 ((2 3) 4)  ((2 3) 4)
            """
            self.q = []

        def empty(self):
            return len(self.q) == 0

        def add(self, leaf):
            if len(self.q) == 0:  # Not in any list
                return False
            root_cons, tar_cons = self.q[-1]
            if tar_cons.car is None:  # (NIL . NIL)
                # Should only be reached on 1st call immediately after `start_list`
                tar_cons.car = leaf
            else:  # (x . NIL)
                assert tar_cons.cdr is None
                tar_cons.cdr = Cons(car=leaf, cdr=None)  # (x . (leaf . None))
                self.q[-1] = root_cons, tar_cons.cdr
            return True

        def start_list(self):
            cons = Cons(car=None, cdr=None)
            self.q.append((cons, cons))

        def close_list(self):
            cons, _ = self.q.pop()
            if len(self.q) == 0:
                return cons
            self.add(cons)

        def clear(self):
            self.q.clear()

    def __init__(self):
        self.cons_builder = self.ConsBuilder()
        self.result = []
        self.symbol_build = ''
        self.prev_symbol = ''

    def lex(self, code: str) -> list:
        #  Returns list of Atoms/Cons to be evaluated
        self.cons_builder.clear()
        self.result.clear()
        self.symbol_build = ''
        self.prev_symbol = ''

        # Case-insensitive names, comments begin w/ `;`
        lines = list(map(lambda l: l if ';' not in l else l[:l.index(';')], code.strip().upper().split('\n')))
        for line_num, line in enumerate(lines):
            for char in line:
                if char == '"':
                    pass
                elif char == ' ':
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

            # Add `if val.startswith("#")...

            if not self.cons_builder.add(atom):
                self.result.append(atom)
            self.prev_symbol = self.symbol_build
            self.symbol_build = ''


class Evaluator:
    def evaluate(self, obj, env: Environment):
        if type(obj) is Value:
            pass
        elif type(obj) is Symbol:
            # Should only be a Symbol holding a variable name;
            # Function names should be (function x) in a list, not evaluated as a Symbol
            try:
                return env.get_var(obj)
            except KeyError:
                raise Error.UndefinedVariableException
        elif type(obj) is Cons:
            # (func . args)
            function = obj.car
            arguments = obj.cdr
            self.call_function(function, arguments, env)
        else:
            raise Exception(obj)

    def call_function(self, function, arguments, env):
        pass


x = Lexer().lex('(1 (2 3 4) 5)')
pass
