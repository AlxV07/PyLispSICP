# http://www.lispworks.com/documentation/lw50/CLHS/Body/03_aba.htm
# 3.1.2.1 Form Evaluation
# Forms fall into three categories: symbols, conses, and self-evaluating objects.

# Symbol & self-evaluating object forms are non-cons objects, or atoms.
# Self-evaluating objects are set values such as numbers and strings.
# Symbols are either variables or symbol macros (expands to function).

# A cons used as a form is called a compound form.
# If the car of the form a symbol, it is the name of a function form or a macro form to expand to.
# Otherwise, the car of the form is a lambda expression and the compound form is a lambda form.

# TODO: Environment Lock Binding Violation; Fix up Nth Func; Finish BuiltInFuncs

class Error:
    # Lisp errors
    class IllegalFunctionNameException(Exception): pass

    class UnmatchedParenthesesException(Exception): pass

    class UndefinedFunctionException(Exception): pass

    class UndefinedVariableException(Exception): pass

    class UnmatchedQuotationException(Exception): pass

    class InvalidNOFArgumentsException(Exception): pass

    class IllegalFunctionCallException(Exception): pass

    class SymbolLockBoundViolationException(Exception): pass


class Atom:
    # Non-cons object
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class Cons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        if self.cdr is BuiltIns.NIL:
            return f'({str(self.car)})'
        return f'({str(self.car)} {"" if type(self.car) is Cons or type(self.cdr) is Cons else ". "}{str(self.cdr)})'


class Symbol(Atom):
    # Represents name of a binding in the environment
    pass


class DefinedFunc:
    def __init__(self, parameters: Cons, expression: Cons):
        self.parameters = parameters
        self.expression = expression


class Environment:
    def __init__(self, var_bindings: dict, func_bindings: dict):
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
    class NilClass:
        # SelfEvalObj
        def __str__(self):
            return "NIL"

        def __bool__(self):
            return False

    NIL = NilClass()

    class TClass:
        def __str__(self):
            return "T"

        def __bool__(self):
            return True

    T = TClass()

    class Number(Atom):
        # SelfEvalObj
        pass

    class String(Atom):
        # SelfEvalObj
        def __str__(self):
            return f"'{self.val}'"

    class BuiltInFunction:
        def __init__(self, eval_method):
            self.eval_method = eval_method

        def call(self, arguments: Cons, env: Environment):
            pass

        @staticmethod
        def at_least_args_check(arguments: Cons, nof_args: int):
            if nof_args == 0: return
            arg = arguments
            count = 0
            while arg is not BuiltIns.NIL:
                count += 1
                if count == nof_args:
                    return
                arg = arg.cdr
            raise Error.InvalidNOFArgumentsException

        @staticmethod
        def exact_args_check(arguments: Cons, nof_args: int):
            arg = arguments
            count = 0
            while arg is not BuiltIns.NIL:
                count += 1
                if count == nof_args:
                    if arg.cdr is not BuiltIns.NIL:
                        raise Error.InvalidNOFArgumentsException
                    return
                arg = arg.cdr
            raise Error.InvalidNOFArgumentsException

    class AddFunc(BuiltInFunction):
        def call(self, arguments, env):
            total = 0
            argument = arguments
            while argument is not BuiltIns.NIL:
                total += self.eval_method(argument.car, env).val
                argument = argument.cdr
            return BuiltIns.Number(total)

    class DiffFunc(BuiltInFunction):
        def call(self, arguments, env):
            self.at_least_args_check(arguments, 1)
            total = 0 if arguments.cdr is BuiltIns.NIL else None  # Only 1 arg?
            argument = arguments
            while argument is not BuiltIns.NIL:
                if total is None:  # Set total to start subtract from
                    total = self.eval_method(argument.car, env).val
                else:
                    total -= self.eval_method(argument.car, env).val
                argument = argument.cdr
            return BuiltIns.Number(total)

    class ProdFunc(BuiltInFunction):
        def call(self, arguments, env):
            total = 1
            argument = arguments
            while argument is not BuiltIns.NIL:
                total *= self.eval_method(argument.car, env).val
                argument = argument.cdr
            return BuiltIns.Number(total)

    class QuotFunc(BuiltInFunction):
        def call(self, arguments, env):
            self.at_least_args_check(arguments, 1)
            total = 1 if arguments.cdr is BuiltIns.NIL else None  # Only 1 arg?
            argument = arguments
            while argument is not BuiltIns.NIL:
                if total is None:  # Set total to start dividing
                    total = self.eval_method(argument.car, env).val
                else:
                    total /= self.eval_method(argument.car, env).val
                argument = argument.cdr
            return BuiltIns.Number(total)

    class EqualFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            self.at_least_args_check(arguments, 1)
            check = None
            argument = arguments
            while argument is not BuiltIns.NIL:
                if check is None:
                    check = self.eval_method(argument.car, env).val
                else:
                    if check != self.eval_method(argument.car, env).val:
                        return BuiltIns.NIL
                argument = argument.cdr
            return BuiltIns.T

    class GreaterThanFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            self.exact_args_check(arguments, 2)
            if self.eval_method(arguments.car, env).val > self.eval_method(arguments.cdr.car, env).val:
                return BuiltIns.T
            return BuiltIns.NIL

    class LessThanFunc(GreaterThanFunc):
        def call(self, arguments: Cons, env: Environment):
            self.exact_args_check(arguments, 2)
            if self.eval_method(arguments.car, env).val < self.eval_method(arguments.cdr.car, env).val:
                return BuiltIns.T
            return BuiltIns.NIL

    class NotFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            self.exact_args_check(arguments, 1)
            if self.eval_method(arguments.car, env) is BuiltIns.T:
                return BuiltIns.NIL
            return BuiltIns.T

    class DefunFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            self.at_least_args_check(arguments, 2)
            if type(arguments.car) is not Symbol:
                raise Error.IllegalFunctionNameException
            env.bind_func(arguments.car, DefinedFunc(parameters=arguments.cdr.car,
                                                     expression=arguments.cdr.cdr))
            return arguments.car  # Func name

    class ConsFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            self.exact_args_check(arguments, 2)
            return Cons(self.eval_method(arguments.car, env),
                        self.eval_method(arguments.cdr.car, env))

    class ListFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            return arguments

    class CarFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            self.exact_args_check(arguments, 1)
            return self.eval_method(arguments.car, env).car

    class CdrFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            self.exact_args_check(arguments, 1)
            return self.eval_method(arguments.car, env).cdr

    # Fix up NthFunc using other built-ins
    class NthFunc(BuiltInFunction):
        def call(self, arguments: Cons, env: Environment):
            if arguments is BuiltIns.NIL or \
                    type(arguments.cdr) is Cons and arguments.cdr.cdr is not BuiltIns.NIL:  # > 2 arguments
                raise Error.InvalidNOFArgumentsException

            n = self.eval_method(arguments.car, env).val
            r = self.eval_method(arguments.cdr.car, env)
            while n > 0:
                r = r.cdr
                if r is BuiltIns.NIL:
                    return r
                n -= 1
            return r.car


class Lexer:
    class ConsBuilder:
        def __init__(self):
            """
            root & tar cons for easy bookkeeping: what to return and what to add to, respectively
            When adding, assert that `target.cdr` is `NIL`, then set `target.cdr` to `Cons(val, NIL)`

            Note: trailing `NIL` is redacted from root reprs:

            ToBeConsed: (1 2 3 4)
            Root          |  Target
            (1 (2))         (2 NIL)
            (1 (2 3))       (3 NIL)
            (1 (2 (3 4)))   (4 NIL)

            ToBeConsed: (1 (2 3) 4)
            Root         |         Target
            (1)                   (1 NIL)
            (2 3)                 (3 NIL)
            (1 (2 3))         ((2 3) NIL)
            (1 ((2 3) 4))         (4 NIL)
            """
            self.q = []

        def empty(self):
            return len(self.q) == 0

        def add(self, leaf):
            if len(self.q) == 0:  # Not in any list
                return False
            root_cons, tar_cons = self.q[-1]
            if tar_cons.car is None:  # (None . NIL)
                # Should only be reached on 1st call immediately after `start_list`
                tar_cons.car = leaf
            else:  # (x . NIL)
                assert tar_cons.cdr is BuiltIns.NIL
                tar_cons.cdr = Cons(car=leaf, cdr=BuiltIns.NIL)  # (x . (leaf . NIL))
                self.q[-1] = root_cons, tar_cons.cdr
            return True

        def start_list(self):
            cons = Cons(car=None, cdr=BuiltIns.NIL)
            self.q.append((cons, cons))

        def close_list(self):
            cons, _ = self.q.pop()
            if cons.car is None:  # Empty list
                cons = BuiltIns.NIL
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
        lines = list(map(lambda l: l if ';' not in l else l[:l.index(';')], code.strip().split('\n')))
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
                atom = BuiltIns.String(str(self.symbol_build))
                self.string_building = False
            else:
                try:
                    atom = BuiltIns.Number(int(self.symbol_build))
                except ValueError:
                    try:
                        atom = BuiltIns.Number(float(self.symbol_build))
                    except ValueError:
                        atom = Symbol(self.symbol_build.upper())
            # If `atom` is outside list:
            if not self.cons_builder.add(atom):
                self.result.append(atom)
            self.prev_symbol = self.symbol_build
            self.symbol_build = ''


class Evaluator:
    def __init__(self):
        global_vars = {
            "NIL": BuiltIns.NIL,
            "T": BuiltIns.T,
        }
        global_funcs = {
            "+": BuiltIns.AddFunc(self.evaluate),
            "-": BuiltIns.DiffFunc(self.evaluate),
            "*": BuiltIns.ProdFunc(self.evaluate),
            "/": BuiltIns.QuotFunc(self.evaluate),
            "CONS": BuiltIns.ConsFunc(self.evaluate),
            "CAR": BuiltIns.CarFunc(self.evaluate),
            "CDR": BuiltIns.CdrFunc(self.evaluate),
            "LIST": BuiltIns.ListFunc(self.evaluate),
            "NTH": BuiltIns.NthFunc(self.evaluate),
            "DEFUN": BuiltIns.DefunFunc(self.evaluate),
            "LAMBDA": None,
            "DEFVAR": None,
            "FUNCTION": None,
            "QUOTE": None,
            "FUNCALL": None,
            "IF": None,
            "=": BuiltIns.EqualFunc(self.evaluate),
            ">": BuiltIns.GreaterThanFunc(self.evaluate),
            "<": BuiltIns.LessThanFunc(self.evaluate),
            "NOT": BuiltIns.NotFunc(self.evaluate),
            "COND": None,
            "PRINT": None,
        }
        self.global_env = Environment(global_vars, global_funcs)

    def evaluate(self, obj, env: Environment):
        if obj is BuiltIns.NIL or type(obj) is BuiltIns.Number or type(obj) is BuiltIns.String:
            # SelfEvalObjs
            return obj
        elif type(obj) is Symbol:
            # Should only be a Symbol representing a variable name;
            # Function names should be evaluated by `FUNCTION` in (function x), not evaluated as a Symbol
            try:
                return env.get_var(obj)
            except KeyError:
                raise Error.UndefinedVariableException(obj)
        elif type(obj) is Cons:
            # (func . args)
            if type(obj.car) is not Symbol:
                raise Error.IllegalFunctionCallException(obj)
            try:
                function = env.get_func(obj.car)
            except KeyError:
                raise Error.UndefinedFunctionException(obj)
            arguments = obj.cdr
            return self.call_function(function, arguments, env)
        else:
            raise Exception(obj)

    def call_function(self, function, arguments: Cons, env: Environment):
        if issubclass(type(function), BuiltIns.BuiltInFunction):
            return function.call(arguments, env)  # Use built-in implementation
        assert type(function) is DefinedFunc
        lexical_env = Environment(*env.copy())  # Env to run function inside
        parameter = function.parameters
        argument = arguments
        while parameter is not BuiltIns.NIL:  # Binding values to parameters
            if argument is BuiltIns.NIL:
                raise Error.InvalidNOFArgumentsException
            lexical_env.bind_var(parameter.car, self.evaluate(argument.car, lexical_env))
            parameter = parameter.cdr
            argument = argument.cdr
        e = function.expression
        while e is not BuiltIns.NIL:  # Evaluating expressions in function; return result of last evaluation
            result = self.evaluate(e.car, lexical_env)
            if e.cdr is BuiltIns.NIL:
                return result
            else:
                e = e.cdr


lexer = Lexer()
evaluator = Evaluator()
lexed = lexer.lex("""
(defun a (b c d e) (+ b c) d e)
(a 1 (+ 2 3) 1207490 (- 10 10 50 -50 9))
(list 1 2 3 4)
(cons () 1)
(defun a () (+ 1 3))
(a)
"hi"
(not (not (= 0 (- 1 1))))
(> 1 0)
(not (< 1 (+ 200 123)))
(- 5 3 1.0)
(+)
(* 1 2 3 4 5)
(= (/ 5 1 (+ 2 (- 5 2) ) 2) 0.5 (/ 2))
""")
print(lexed)
for exp in lexed:
    print(evaluator.evaluate(exp, evaluator.global_env))
