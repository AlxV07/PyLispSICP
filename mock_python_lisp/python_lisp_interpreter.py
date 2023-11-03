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
    class UnmatchedQuotationException(Exception): pass
    class InvalidNOFArgumentsException(Exception): pass
    class IllegalFunctionIdentifierException(Exception): pass


class Atom:
    # Non-cons object
    def __init__(self, val):
        self.val = val


class SelfEvaluatingObject(Atom):
    pass


class Number(SelfEvaluatingObject):
    pass


class String(SelfEvaluatingObject):
    pass


class Symbol(Atom):
    # Represents name of a binding in the environment
    pass


class Function:
    def __init__(self, parameters, form):
        self.parameters = parameters
        self.form = form


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


class Lexer:
    class ConsBuilder:
        def __init__(self):
            """
            root & tar cons for easy bookkeeping: what to return and what to add to, respectively

            Note: trailing `None` is redacted from following examples:
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
        self.string_building = False

    def lex(self, code: str) -> list:
        #  Returns list of Atoms/Cons to be evaluated
        self.cons_builder.clear()
        self.result.clear()
        self.symbol_build = ''
        self.prev_symbol = ''
        self.string_building = False

        # Case-insensitive names, comments begin w/ `;`
        lines = list(map(lambda l: l if ';' not in l else l[:l.index(';')], code.strip().upper().split('\n')))
        for line in lines:
            for char in line:
                if char == '"':
                    if not self.string_building:
                        self.string_building = True
                    else:
                        self.exit_atom_build()
                elif self.string_building:
                    self.enter_atom_build(char)
                    continue
                elif char == ' ':
                    self.exit_atom_build()
                elif char == '(':
                    self.exit_atom_build()
                    self.cons_builder.start_list()
                elif char == ')':
                    self.exit_atom_build()
                    try:
                        returned_list = self.cons_builder.close_list()
                    except IndexError:
                        raise Error.UnmatchedParenthesesException()
                    if returned_list is not None:
                        self.result.append(returned_list)
                else:
                    self.enter_atom_build(char)
        if self.string_building:
            raise Error.UnmatchedQuotationException()
        if not self.cons_builder.empty():
            raise Error.UnmatchedParenthesesException()
        return self.result

    def enter_atom_build(self, char):
        self.symbol_build += char

    def exit_atom_build(self):
        if len(self.symbol_build) > 0:
            # `if val.startswith("#")...

            # `if val.startswith("'")...

            if self.string_building:
                atom = String(str(self.symbol_build))
                self.string_building = False
            else:
                try:
                    atom = Number(float(self.symbol_build))
                except ValueError:
                    atom = Symbol(self.symbol_build)
            # If `atom` is outside list:
            if not self.cons_builder.add(atom):
                self.result.append(atom)
            self.prev_symbol = self.symbol_build
            self.symbol_build = ''


class BuiltIns:
    class BuiltInFunction:
        def __init__(self, eval_method):
            self.eval_method = eval_method

        def call(self, arguments: Cons, env: Environment):
            pass

        @staticmethod
        def arg_count_check(expected: int, actual: int, exact: bool):
            if exact:
                if actual != expected:
                    raise Error.InvalidNOFArgumentsException
            else:
                if actual < expected:
                    raise Error.InvalidNOFArgumentsException

    class Add(BuiltInFunction):
        def call(self, arguments, env):
            total = 0
            arg_count = 0
            argument = arguments
            while argument is not None:
                val = self.eval_method(argument.car, env).val
                total += val
                argument = argument.cdr
                arg_count += 1
            self.arg_count_check(2, arg_count, False)
            return Number(total)

    class Diff(BuiltInFunction):
        def call(self, arguments, env):
            arg_count = 0
            total = 0
            argument = arguments
            while argument is not None:
                val = self.eval_method(argument.car, env).val
                if arg_count == 0:
                    total = val
                else:
                    total -= val
                argument = argument.cdr
                arg_count += 1
            self.arg_count_check(2, arg_count, False)
            return Number(total)

    class Prod(BuiltInFunction):
        def call(self, arguments, env):
            arg_count = 0
            total = 1
            argument = arguments
            while argument is not None:
                val = self.eval_method(argument.car, env).val
                total *= val
                argument = argument.cdr
                arg_count += 1
            self.arg_count_check(2, arg_count, False)
            return Number(total)

    class Quot(BuiltInFunction):
        def call(self, arguments, env):
            arg_count = 0
            total = 0
            argument = arguments
            while argument is not None:
                val = self.eval_method(argument.car, env).val
                if arg_count == 0:
                    total = val
                else:
                    total /= val
                argument = argument.cdr
                arg_count += 1
            self.arg_count_check(2, arg_count, True)
            return Number(total)

    class Cons(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            return arguments


class Evaluator:
    def __init__(self):
        global_vars = {
            "NIL": None,
            "T": None,
        }
        global_funcs = {
            "+": BuiltIns.Add(self.evaluate),
            "-": BuiltIns.Diff(self.evaluate),
            "*": BuiltIns.Prod(self.evaluate),
            "/": BuiltIns.Quot(self.evaluate),
            "CONS": BuiltIns.Cons(self.evaluate),
            "CAR": None,
            "CDR": None,
            "LIST": None,
            "LAMBDA": None,
            "DEFVAR": None,
            "DEFUN": None,
            "FUNCALL": None,
            "IF": None,
            "COND": None,
            "PRINT": None,
        }
        self.global_env = Environment(global_vars, global_funcs)

    def evaluate(self, obj, env: Environment):
        if type(obj) is Number or type(obj) is String:
            return obj
        elif type(obj) is Symbol:
            # Should only be a Symbol holding a variable name;
            # Function names should be (function x) in a list, not evaluated as a Symbol
            try:
                return env.get_var(obj)
            except KeyError:
                raise Error.UndefinedVariableException(obj)
        elif type(obj) is Cons:
            # (func . args)
            try:
                if type(obj.car) is not Symbol:
                    raise Error.IllegalFunctionIdentifierException(obj)
                function = env.get_func(obj.car)
            except KeyError:
                raise Error.UndefinedFunctionException(obj)
            arguments = obj.cdr
            if issubclass(type(function), BuiltIns.BuiltInFunction):
                return function.call(arguments, env)
            else:
                return self.call_function(function, arguments, env)
        else:
            raise Exception(obj)

    def call_function(self, function: Function, arguments: Cons, env: Environment):
        lexical_env = Environment(*env.copy())  # Env to run function inside
        parameter = function.parameters
        argument = arguments
        while parameter is not None:  # Binding values to parameters in env
            lexical_env.bind_var(parameter.car, self.evaluate(argument.car, lexical_env))
            parameter = parameter.cdr
            argument = arguments.cdr
        return self.evaluate(function.form, lexical_env)


lexer = Lexer()
evaluator = Evaluator()
lexed = lexer.lex("""
(* (/ (+ 1 (+ 2 3)) 2) 3 3)
(cons 1 2)
""")
result = evaluator.evaluate(lexed[0], evaluator.global_env)
print(result)
print(result.val)
result = evaluator.evaluate(lexed[1], evaluator.global_env)
print(result)
print(result.car.val)
print(result.cdr.car.val)
pass
