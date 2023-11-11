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
    class IllegalFunctionNameException(Exception): pass

    class IllegalVariableNameException(Exception): pass

    class UnmatchedParenthesesException(Exception): pass

    class UndefinedFunctionException(Exception): pass

    class UndefinedVariableException(Exception): pass

    class UnmatchedQuotationException(Exception): pass

    class InvalidNOFArgumentsException(Exception): pass

    class IllegalFunctionCallException(Exception): pass

    class SymbolLockBoundViolationException(Exception): pass


class Cons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        if self.cdr is BuiltIns.NIL:
            return f'({str(self.car)})'
        return f'({str(self.car)} {"" if type(self.car) is Cons or type(self.cdr) is Cons else ". "}{str(self.cdr)})'


class Environment:
    def __init__(self, var_bindings: dict, func_bindings: dict):
        self.var_bindings = var_bindings
        self.func_bindings = func_bindings

    def bind_var(self, symbol, item):
        self.var_bindings[symbol.name] = item

    def bind_func(self, symbol, item):
        self.func_bindings[symbol.name] = item

    def get_var(self, symbol):
        return self.var_bindings[symbol.name]

    def get_func(self, symbol):
        return self.func_bindings[symbol.name]

    def copy(self):
        return self.var_bindings.copy(), self.func_bindings.copy()


class Function:
    def __init__(self, name, parameters, expression):
        self.name = name
        self.parameters = parameters
        self.expression = expression

    def __str__(self):
        return f'#<FUNCTION {str(self.name)}>'

    def call(self, arguments: Cons, env: Environment):
        lexical_env = Environment(*env.copy())  # Env to run function inside
        parameter = self.parameters
        argument = arguments
        while parameter is not BuiltIns.NIL and argument is not BuiltIns.NIL:  # Binding values to parameters
            lexical_env.bind_var(parameter.car, Evaluator.evaluate(argument.car, env))
            parameter = parameter.cdr
            argument = argument.cdr
        if parameter is not BuiltIns.NIL or argument is not BuiltIns.NIL:
            raise Error.InvalidNOFArgumentsException
        e = self.expression
        while e is not BuiltIns.NIL:  # Evaluating expressions in function; return result of last evaluation
            result = Evaluator.evaluate(e.car, lexical_env)
            if e.cdr is BuiltIns.NIL:
                return result
            else:
                e = e.cdr


class BuiltIns:

    class NilClass:
        def __str__(self):
            return "NIL"

    NIL = NilClass()

    class TClass:
        def __str__(self):
            return "T"

    T = TClass()

    class Symbol:
        def __init__(self, name):
            # Represents name of a binding in the environment
            self.name = name

        def __str__(self):
            return self.name

    class BuiltInFunctions:
        class BuiltInFunction(Function):
            def __init__(self, name):
                super().__init__(name, None, None)

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

            def call(self, arguments: Cons, env: Environment):
                pass

        class AddFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('+')

            def call(self, arguments: Cons, env: Environment):
                total = 0
                argument = arguments
                while argument is not BuiltIns.NIL:
                    total += Evaluator.evaluate(argument.car, env)
                    argument = argument.cdr
                return total

        class DiffFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('-')

            def call(self, arguments: Cons, env: Environment):
                self.at_least_args_check(arguments, 1)
                total = 0 if arguments.cdr is BuiltIns.NIL else None  # Only 1 arg?
                argument = arguments
                while argument is not BuiltIns.NIL:
                    if total is None:  # Set total to start subtract from
                        total = Evaluator.evaluate(argument.car, env)
                    else:
                        total -= Evaluator.evaluate(argument.car, env)
                    argument = argument.cdr
                return total

        class ProdFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('*')

            def call(self, arguments: Cons, env: Environment):
                total = 1
                argument = arguments
                while argument is not BuiltIns.NIL:
                    total *= Evaluator.evaluate(argument.car, env)
                    argument = argument.cdr
                return total

        class QuotFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('/')

            def call(self, arguments: Cons, env: Environment):
                self.at_least_args_check(arguments, 1)
                total = 1 if arguments.cdr is BuiltIns.NIL else None  # Only 1 arg?
                argument = arguments
                while argument is not BuiltIns.NIL:
                    if total is None:  # Set total to start dividing
                        total = Evaluator.evaluate(argument.car, env)
                    else:
                        total /= Evaluator.evaluate(argument.car, env)
                    argument = argument.cdr
                return total

        class EqualFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('=')

            def call(self, arguments: Cons, env: Environment):
                self.at_least_args_check(arguments, 1)
                check = None
                argument = arguments
                while argument is not BuiltIns.NIL:
                    if check is None:
                        check = Evaluator.evaluate(argument.car, env)
                    else:
                        if check != Evaluator.evaluate(argument.car, env):
                            return BuiltIns.NIL
                    argument = argument.cdr
                return BuiltIns.T

        class GreaterThanFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('\'>\'')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 2)
                if Evaluator.evaluate(arguments.car, env) > Evaluator.evaluate(arguments.cdr.car, env):
                    return BuiltIns.T
                return BuiltIns.NIL

        class LessThanFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('\'<\'')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 2)
                if Evaluator.evaluate(arguments.car, env) < Evaluator.evaluate(arguments.cdr.car, env):
                    return BuiltIns.T
                return BuiltIns.NIL

        class NotFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('NOT')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 1)
                if Evaluator.evaluate(arguments.car, env) is BuiltIns.T:
                    return BuiltIns.NIL
                return BuiltIns.T

        class IfFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('IF')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 3)
                #  (if T 1 0) -> arguments = (T (1 (0 NIL)))
                if Evaluator.evaluate(arguments.car, env) is BuiltIns.T:
                    return Evaluator.evaluate(arguments.cdr.car, env)
                return Evaluator.evaluate(arguments.cdr.cdr.car, env)

        class DefunFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('DEFUN')

            def call(self, arguments: Cons, env: Environment):
                self.at_least_args_check(arguments, 3)
                if type(arguments.car) is not BuiltIns.Symbol:
                    raise Error.IllegalFunctionNameException
                if BuiltIns.is_symbol_globally_bound(arguments.car):
                    raise Error.SymbolLockBoundViolationException
                env.bind_func(arguments.car, Function(name=arguments.car, parameters=arguments.cdr.car,
                                                      expression=arguments.cdr.cdr))
                return arguments.car  # Func name

        class FunctionFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('FUNCTION')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 1)
                try:
                    return env.get_func(arguments.car)
                except KeyError:
                    raise Error.UndefinedFunctionException

        class FuncallFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('FUNCALL')

            def call(self, arguments: Cons, env: Environment):
                self.at_least_args_check(arguments, 1)
                return Evaluator.evaluate(arguments.car, env).call(arguments.cdr, env)

        class ConsFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('CONS')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 2)
                return Cons(Evaluator.evaluate(arguments.car, env),
                            Evaluator.evaluate(arguments.cdr.car, env))

        class ListFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('LIST')

            def call(self, arguments: Cons, env: Environment):
                return arguments

        class CarFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('CAR')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 1)
                return Evaluator.evaluate(arguments.car, env).car

        class CdrFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('CDR')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 1)
                return Evaluator.evaluate(arguments.car, env).cdr

        class PrintFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('PRINT')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 1)
                print(evaluator.evaluate(arguments.car, env))
                return BuiltIns.NIL

        class LetFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('LET')

            def call(self, arguments: Cons, env: Environment):
                self.at_least_args_check(arguments, 2)
                lexical_env = Environment(*env.copy())
                parameter = arguments.car
                while parameter is not BuiltIns.NIL:
                    BuiltIns.global_funcs['DEFPARAMETER'].call(parameter.car, lexical_env)
                    parameter = parameter.cdr
                e = arguments.cdr
                while e is not BuiltIns.NIL:  # Evaluating expressions in function; return result of last evaluation
                    result = Evaluator.evaluate(e.car, lexical_env)
                    if e.cdr is BuiltIns.NIL:
                        return result
                    else:
                        e = e.cdr

        class QuoteFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('QUOTE')

            def call(self, arguments: Cons, env: Environment):
                self.exact_args_check(arguments, 1)
                return arguments.car

        class DefparameterFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('DEFPARAMETER')

            def call(self, arguments: Cons, env: Environment):
                if type(arguments.car) is not BuiltIns.Symbol:
                    raise Error.IllegalVariableNameException
                if BuiltIns.is_symbol_globally_bound(arguments.car):
                    raise Error.SymbolLockBoundViolationException
                self.exact_args_check(arguments, 2)
                env.bind_var(arguments.car, Evaluator.evaluate(arguments.cdr.car, env))

        class DefvarFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('DEFVAR')

            def call(self, arguments: Cons, env: Environment):
                if type(arguments.car) is not BuiltIns.Symbol:
                    raise Error.IllegalVariableNameException
                if BuiltIns.is_symbol_globally_bound(arguments.car):
                    raise Error.SymbolLockBoundViolationException
                self.exact_args_check(arguments, 2)
                try:
                    env.get_var(arguments.car)
                except KeyError:
                    env.bind_var(arguments.car, Evaluator.evaluate(arguments.cdr.car, env))

        class CondFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('COND')

            def call(self, arguments: Cons, env: Environment):
                argument = arguments
                while argument is not BuiltIns.NIL:
                    condition = argument.car.car
                    if Evaluator.evaluate(condition, env) is BuiltIns.T:
                        return Evaluator.evaluate(argument.car.cdr.car, env)
                    argument = argument.cdr
                return BuiltIns.NIL

        class LambdaFunc(BuiltInFunction):
            def __init__(self):
                super().__init__('LAMBDA')

            def call(self, arguments: Cons, env: Environment):
                self.at_least_args_check(arguments, 2)
                return Function(name='LAMBDA', parameters=arguments.car, expression=arguments.cdr)

    global_vars = {
        "NIL": NIL,
        "T": T,
    }
    global_funcs = {
        "+": BuiltInFunctions.AddFunc(),
        "-": BuiltInFunctions.DiffFunc(),
        "*": BuiltInFunctions.ProdFunc(),
        "/": BuiltInFunctions.QuotFunc(),
        "CAR": BuiltInFunctions.CarFunc(),
        "CDR": BuiltInFunctions.CdrFunc(),
        "CONS": BuiltInFunctions.ConsFunc(),
        "LIST": BuiltInFunctions.ListFunc(),
        "DEFUN": BuiltInFunctions.DefunFunc(),
        "DEFPARAMETER": BuiltInFunctions.DefparameterFunc(),
        "DEFVAR": BuiltInFunctions.DefvarFunc(),
        "LET": BuiltInFunctions.LetFunc(),
        "FUNCTION": BuiltInFunctions.FunctionFunc(),
        "FUNCALL": BuiltInFunctions.FuncallFunc(),
        "LAMBDA": BuiltInFunctions.LambdaFunc(),
        "IF": BuiltInFunctions.IfFunc(),
        "COND": BuiltInFunctions.CondFunc(),
        "=": BuiltInFunctions.EqualFunc(),
        ">": BuiltInFunctions.GreaterThanFunc(),
        "<": BuiltInFunctions.LessThanFunc(),
        "NOT": BuiltInFunctions.NotFunc(),
        "PRINT": BuiltInFunctions.PrintFunc(),
        "QUOTE": BuiltInFunctions.QuoteFunc(),
    }
    global_env = Environment(global_vars, global_funcs)

    @staticmethod
    def is_symbol_globally_bound(symbol: Symbol) -> bool:
        return BuiltIns.global_env.func_bindings.get(symbol.name, None) is not None or \
                        BuiltIns.global_env.var_bindings.get(symbol.name, None) is not None


class Parser:
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
        self.string_building = False

    def parse(self, code: str) -> list:
        #  Returns list of Atoms/Cons to be evaluated
        self.cons_builder.clear()
        self.result.clear()
        self.symbol_build = ''
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
            if self.string_building:
                atom = str(self.symbol_build)
                self.string_building = False
            elif self.symbol_build.startswith("'"):
                self.cons_builder.start_list()
                self.cons_builder.add(BuiltIns.Symbol('QUOTE'))
                self.symbol_build = self.symbol_build[1:]
                self.exit_atom_build()
                self.cons_builder.close_list()
                return
            elif self.symbol_build.startswith("#'"):
                self.cons_builder.start_list()
                self.cons_builder.add(BuiltIns.Symbol('FUNCTION'))
                self.symbol_build = self.symbol_build[2:]
                self.exit_atom_build()
                self.cons_builder.close_list()
                return
            else:
                try:
                    atom = int(self.symbol_build)
                except ValueError:
                    try:
                        atom = float(self.symbol_build)
                    except ValueError:
                        atom = BuiltIns.Symbol(self.symbol_build.upper())
            # If `atom` is outside list:
            if not self.cons_builder.add(atom):
                self.result.append(atom)
            self.symbol_build = ''


class Evaluator:
    @staticmethod
    def evaluate(obj, env: Environment):
        if obj is BuiltIns.NIL or type(obj) is int or type(obj) is float or type(obj) is str:
            # SelfEvalObjs
            return obj
        elif type(obj) is BuiltIns.Symbol:
            # Should only be a Symbol representing a variable name;
            # Function names should be evaluated by `FUNCTION` in (function x), not evaluated as a Symbol
            try:
                return env.get_var(obj)
            except KeyError:
                raise Error.UndefinedVariableException(obj)
        elif type(obj) is Cons:
            # (func . args)
            if type(obj.car) is not BuiltIns.Symbol:
                raise Error.IllegalFunctionCallException(obj)
            try:
                function = env.get_func(obj.car)
            except KeyError:
                raise Error.UndefinedFunctionException(obj)
            arguments = obj.cdr
            try:
                return function.call(arguments, env)
            except AttributeError:
                raise Error.IllegalFunctionCallException
        else:
            raise Exception(obj)


parser = Parser()
evaluator = Evaluator()
parsed = parser.parse("""
(defun square (x) (* x x))
(defun abs (x)
    (if (< x 0)
        (* x -1)
        x))
(defun average (x y) 
    (/ (+ x y) 2))
(defun good-enough? (guess x)
    (< (abs (- (square guess) x)) 0.001))
(defun improve (guess x)
    (average guess (/ x guess)))
(defun sqrt-iter (guess x)
    (if (good-enough? guess x)
        guess
        (sqrt-iter (improve guess x) x)))
(defun sqrt (x)
    (sqrt-iter 1.0 x))
(print (sqrt 4))
(print (sqrt 64)) 
(print (sqrt 100))

(print 
    (let ((x 1) (y 2)) 
        (print (+ x y))
        (print (- y x))
        x))
        
(print (function print))
;(print (function (quote print)))
(defun p () 0)
;(print p)
(print 'p)
(print (function p))

(defparameter p 124)
(print p)
(defparameter p 125)
(print p)
(defvar p 126)
(print p)

(defvar o 127)
(print o)
(defvar o 128)
(print o)

(print (cond
((< 1 0) "sup")
((> 1 0) "nope")
))

(defun x (func)
    (funcall func 5))
(defun a (p) (+ p 1))
(defun b (p) (+ p 2))
(print (x #'a))
(print (x #'b))

(print (x 
    (lambda (a) (+ a 3))
))
""")
run_env = Environment(*BuiltIns.global_env.copy())
for exp in parsed: evaluator.evaluate(exp, run_env)
