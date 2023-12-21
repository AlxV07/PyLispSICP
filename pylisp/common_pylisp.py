class Error:
    # Lisp errors
    class IllegalProcedureNameException(Exception): pass

    class IllegalVariableNameException(Exception): pass

    class UnmatchedParenthesesException(Exception): pass

    class UndefinedProcedureException(Exception): pass

    class UndefinedVariableException(Exception): pass

    class UnmatchedQuotationException(Exception): pass

    class InvalidNOFArgumentsException(Exception): pass

    class IllegalFunctionCallException(Exception): pass

    class SymbolLockBoundViolationException(Exception): pass


class Object:
    # All things to be evaluated are objects
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        raise Exception('Undefined Object evaluation:', self)


class Symbol(Object):
    # Represents a binding in the environment
    def evaluate(self, env):
        return env.get_var(self)

    def __str__(self):
        return str(self.value)


class SelfEvaluatingObject(Object):
    def evaluate(self, env):
        return self

    def __str__(self):
        return str(self.value)


class Cons(Object):
    def __init__(self, car, cdr):
        super().__init__('CONS')
        self.car = car
        self.cdr = cdr

    def evaluate(self, env):
        proc = env.get_proc(self.car)
        args = self.cdr
        return proc.evaluate(env, args)

    def __str__(self):
        if self.cdr is BuiltIns.NIL:
            return f'({self.car})'
        s = []
        p = self
        while p is not BuiltIns.NIL:
            if type(p) is not Cons:
                s.append(str(p))
                break
            s.append(str(p.car))
            p = p.cdr
        return f'({" ".join(s)})'


class Environment:
    def __init__(self, var_bindings: dict, proc_bindings: dict):
        self.var_bindings = var_bindings
        self.proc_bindings = proc_bindings

    def bind_var(self, symbol, item):
        if type(symbol) is not Symbol:
            raise Error.IllegalVariableNameException(symbol)
        if BuiltIns.is_symbol_globally_bound(symbol):
            raise Error.SymbolLockBoundViolationException(symbol)
        self.var_bindings[symbol.value] = item

    def bind_proc(self, symbol, item):
        if type(symbol) is not Symbol:
            raise Error.IllegalProcedureNameException(symbol)
        if BuiltIns.is_symbol_globally_bound(symbol):
            raise Error.SymbolLockBoundViolationException(symbol)
        self.proc_bindings[symbol.value] = item

    def get_var(self, symbol):
        if type(symbol) is not Symbol:
            raise Error.IllegalVariableNameException(symbol)
        var = self.var_bindings.get(symbol.value)
        if var is None:
            raise Error.UndefinedVariableException(symbol)
        return var

    def get_proc(self, symbol):
        if type(symbol) is not Symbol:
            raise Error.IllegalProcedureNameException(symbol)
        proc = self.proc_bindings.get(symbol.value)
        if proc is None:
            raise Error.UndefinedProcedureException(symbol)
        return proc

    def copy(self):
        return self.var_bindings.copy(), self.proc_bindings.copy()


class Procedure:
    def __init__(self, name):
        self.name = name

    def evaluate(self, env, args):
        raise Exception('Undefined Procedure evaluation:', self)

    def __str__(self):
        return f'#<FUNCTION {self.name}>'


class UserDefinedProcedure(Procedure):
    def __init__(self, name, parameters, expression):
        super().__init__(name)
        self.parameters = parameters
        self.expression = expression

    def evaluate(self, env, args):
        lexical_env = Environment(*env.copy())
        parameter = self.parameters
        arg = args
        while parameter is not BuiltIns.NIL and arg is not BuiltIns.NIL:  # Binding values to parameters
            lexical_env.bind_var(parameter.car, arg.car.evaluate(env))
            parameter = parameter.cdr
            arg = arg.cdr
        if parameter is not BuiltIns.NIL or arg is not BuiltIns.NIL:  # Left over parameter or argument
            raise Error.InvalidNOFArgumentsException(self)
        e = self.expression
        while e is not BuiltIns.NIL:  # Evaluating expressions in function; return result of last evaluation
            result = e.car.evaluate(lexical_env)
            if e.cdr is BuiltIns.NIL:
                return result
            else:
                e = e.cdr


class BuiltIns:

    class NilClass(SelfEvaluatingObject):
        def __init__(self):
            super().__init__('NIL')

    NIL = NilClass()

    class TClass(SelfEvaluatingObject):
        def __init__(self):
            super().__init__('T')

    T = TClass()

    class Number(SelfEvaluatingObject):
        def __add__(self, other):
            return BuiltIns.Number(self.value + other.value)

        def __sub__(self, other):
            return BuiltIns.Number(self.value - other.value)

        def __mul__(self, other):
            return BuiltIns.Number(self.value * other.value)

        def __truediv__(self, other):
            if other.value == 0:
                raise ValueError("Division by zero is not allowed")
            return BuiltIns.Number(self.value / other.value)

        def __gt__(self, other):
            return self.value > other.value

        def __lt__(self, other):
            return self.value < other.value

        def __ge__(self, other):
            return self.value >= other.value

        def __le__(self, other):
            return self.value <= other.value

        def __eq__(self, other):
            return self.value == other.value

    class String(SelfEvaluatingObject): pass

    class BuiltInProcs:
        class ConsFunc(Procedure):
            def __init__(self):
                super().__init__('CONS')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL or  # 1 arg
                        args.cdr.cdr is not BuiltIns.NIL):  # > 2 args
                    raise Error.InvalidNOFArgumentsException(self)
                return Cons(args.car.evaluate(env),
                            args.cdr.car.evaluate(env))

        class CarFunc(Procedure):
            def __init__(self):
                super().__init__('CAR')

            def call(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is not BuiltIns.NIL):  # > 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                return args.car.evaluate(env).car

        class CdrFunc(Procedure):
            def __init__(self):
                super().__init__('CDR')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is not BuiltIns.NIL):  # > 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                return args.car.evaluate(env).cdr

        class ListFunc(Procedure):
            def __init__(self):
                super().__init__('LIST')

            def evaluate(self, env, args):
                if args is BuiltIns.NIL:
                    return args
                a = args
                while a is not BuiltIns.NIL:
                    a.car = a.car.evaluate(env)
                    a = a.cdr
                return args

        class AddProc(Procedure):
            def __init__(self):
                super().__init__('+')

            def evaluate(self, env, args):
                if args is BuiltIns.NIL:
                    return BuiltIns.Number(0)
                else:
                    return args.car.evaluate(env) + BuiltIns.global_funcs.get("+").evaluate(env, args.cdr)

        class DiffProc(Procedure):
            def __init__(self):
                super().__init__('-')

            def evaluate(self, env, args):
                if args is BuiltIns.NIL: raise Error.InvalidNOFArgumentsException(self)  # 0 args
                if args.cdr is BuiltIns.NIL:  # 1 arg
                    total = args.car.evaluate(env) * BuiltIns.Number(-1)
                else:
                    total = args.car.evaluate(env)
                    arg = args.cdr
                    while arg is not BuiltIns.NIL:
                        total -= arg.car.evaluate(env)
                        arg = arg.cdr
                return total

        class ProdProc(Procedure):
            def __init__(self):
                super().__init__('*')

            def evaluate(self, env, args):
                if args is BuiltIns.NIL:
                    return BuiltIns.Number(1)
                else:
                    return args.car.evaluate(env) * BuiltIns.global_funcs.get("*").evaluate(env, args.cdr)

        class QuotProc(Procedure):
            def __init__(self):
                super().__init__('/')

            def evaluate(self, env, args):
                if args is BuiltIns.NIL: raise Error.InvalidNOFArgumentsException(self)  # 0 args
                if args.cdr is BuiltIns.NIL:  # 1 arg
                    total = BuiltIns.Number(1.0) / args.car.evaluate(env)
                else:
                    total = args.car.evaluate(env)
                    arg = args.cdr
                    while arg is not BuiltIns.NIL:
                        total /= arg.car.evaluate(env)
                        arg = arg.cdr
                return total

        class EqualProc(Procedure):
            def __init__(self):
                super().__init__('=')

            def call(self, env, args):
                if args is BuiltIns.NIL: raise Error.InvalidNOFArgumentsException(self)  # 0 args
                check = args.car.evaluate(env)
                arg = args.cdr
                while arg is not BuiltIns.NIL:
                    if args.car.evaluate(env) != check: return BuiltIns.NIL
                    arg = arg.cdr
                return BuiltIns.T

        class GreaterThanProc(Procedure):
            def __init__(self):
                super().__init__('>')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL or  # 1 arg
                        args.cdr.cdr is not BuiltIns.NIL):  # > 2 args
                    raise Error.InvalidNOFArgumentsException(self)
                t1 = args.car.evaluate(env)
                t2 = args.cdr.car.evaluate(env)
                return BuiltIns.T if t1 > t2 else BuiltIns.NIL

        class LessThanProc(Procedure):
            def __init__(self):
                super().__init__('<')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL or  # 1 arg
                        args.cdr.cdr is not BuiltIns.NIL):  # > 2 args
                    raise Error.InvalidNOFArgumentsException(self)
                t1 = args.car.evaluate(env)
                t2 = args.cdr.car.evaluate(env)
                return BuiltIns.T if t1 < t2 else BuiltIns.NIL

        class NotProc(Procedure):
            def __init__(self):
                super().__init__('NOT')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is not BuiltIns.NIL):  # > 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                return BuiltIns.T if args.car.evaluate(env) is BuiltIns.NIL else BuiltIns.NIL

        class IfProc(Procedure):
            def __init__(self):
                super().__init__('IF')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL or  # 1 arg
                        args.cdr.cdr is BuiltIns.NIL or  # 2 args
                        args.cdr.cdr.cdr is not BuiltIns.NIL):  # > 3 args
                    raise Error.InvalidNOFArgumentsException(self)
                #  (if T 1 0) -> arguments = (T (1 (0 NIL)))
                if args.car.evaluate(env) is BuiltIns.T:
                    return args.cdr.car.evaluate(env)
                else:
                    return args.cdr.cdr.car.evaluate(env)

        class CondProc(Procedure):
            def __init__(self):
                super().__init__('COND')

            def evaluate(self, env, args):
                arg = args
                while args is not BuiltIns.NIL:
                    if arg.car.car.evaluate(env) is BuiltIns.T:
                        return arg.car.cdr.car.evaluate(env)
                    arg = arg.cdr
                return BuiltIns.NIL

        class QuoteProc(Procedure):
            def __init__(self):
                super().__init__('QUOTE')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is not BuiltIns.NIL):  # > 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                return args.car

        class DefunProc(Procedure):
            def __init__(self):
                super().__init__('DEFUN')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL or  # 1 arg
                        args.cdr.cdr is BuiltIns.NIL):  # 2 args
                    raise Error.InvalidNOFArgumentsException(self)
                env.bind_proc(args.car, UserDefinedProcedure(name=args.car,
                                                             parameters=args.cdr.car,
                                                             expression=args.cdr.cdr))
                return args.car

        class FunctionProc(Procedure):
            def __init__(self):
                super().__init__('FUNCTION')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is not BuiltIns.NIL):  # > 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                return env.get_proc(args.car)

        class FuncallProc(Procedure):
            def __init__(self):
                super().__init__('FUNCALL')

            def evaluate(self, env, args):
                if args is BuiltIns.NIL: raise Error.InvalidNOFArgumentsException(self)  # 0 args
                return args.car.evaluate(env).evaluate(env, args.cdr)

        class LambdaProc(Procedure):
            def __init__(self):
                super().__init__('LAMBDA')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL):  # 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                return UserDefinedProcedure(name='LAMBDA', parameters=args.car, expression=args.cdr)

        class LetProc(Procedure):
            def __init__(self):
                super().__init__('LET')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL):  # 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                lexical_env = Environment(*env.copy())
                assignment = args.car
                while assignment is not BuiltIns.NIL:
                    if (assignment.car is BuiltIns.NIL or  # 0 args
                            args.car.cdr is BuiltIns.NIL or  # 1 arg
                            args.car.cdr.cdr is not BuiltIns.NIL):  # > 2 arg
                        raise Error.InvalidNOFArgumentsException(assignment)
                    lexical_env.bind_var(assignment.car.car, assignment.car.cdr.car.evaluate(env))
                    assignment = assignment.cdr
                expression = args.cdr
                while expression is not BuiltIns.NIL:  # Evaluating expressions in let; return result of last expression
                    result = expression.car.evaluate(lexical_env)
                    if expression.cdr is BuiltIns.NIL:
                        return result
                    else:
                        expression = expression.cdr

        class DefparameterFunc(Procedure):
            def __init__(self):
                super().__init__('DEFPARAMETER')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL or  # 1 arg
                        args.cdr.cdr is not BuiltIns.NIL):  # > 2 args
                    raise Error.InvalidNOFArgumentsException(self)
                env.bind_var(args.car, args.cdr.car.evaluate(env))

        class DefvarFunc(Procedure):
            def __init__(self):
                super().__init__('DEFVAR')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is BuiltIns.NIL or  # 1 arg
                        args.cdr.cdr is not BuiltIns.NIL):  # > 2 args
                    raise Error.InvalidNOFArgumentsException(self)
                try:
                    env.get_var(args.car)
                except Error.UndefinedVariableException:  # Bind if isn't already bound
                    env.bind_var(args.car, args.cdr.car.evaluate(env))

        class PrintProc(Procedure):
            def __init__(self):
                super().__init__('PRINT')

            def evaluate(self, env, args):
                if (args is BuiltIns.NIL or  # 0 args
                        args.cdr is not BuiltIns.NIL):  # > 1 arg
                    raise Error.InvalidNOFArgumentsException(self)
                print(args.car.evaluate(env))
                return BuiltIns.NIL

    global_vars = {
        "NIL": NIL,
        "T": T,
    }
    global_funcs = {
        "CONS": BuiltInProcs.ConsFunc(),
        "CAR": BuiltInProcs.CarFunc(),
        "CDR": BuiltInProcs.CdrFunc(),
        "LIST": BuiltInProcs.ListFunc(),
        "+": BuiltInProcs.AddProc(),
        "-": BuiltInProcs.DiffProc(),
        "*": BuiltInProcs.ProdProc(),
        "/": BuiltInProcs.QuotProc(),
        ">": BuiltInProcs.GreaterThanProc(),
        "<": BuiltInProcs.LessThanProc(),
        "=": BuiltInProcs.EqualProc(),
        "NOT": BuiltInProcs.NotProc(),
        "IF": BuiltInProcs.IfProc(),
        "COND": BuiltInProcs.CondProc(),
        "QUOTE": BuiltInProcs.QuoteProc(),
        "DEFUN": BuiltInProcs.DefunProc(),
        "FUNCALL": BuiltInProcs.FuncallProc(),
        "FUNCTION": BuiltInProcs.FunctionProc(),
        "LAMBDA": BuiltInProcs.LambdaProc(),
        "LET": BuiltInProcs.LetProc(),
        "DEFPARAMETER": BuiltInProcs.DefparameterFunc(),
        "DEFVAR": BuiltInProcs.DefvarFunc(),
        "PRINT": BuiltInProcs.PrintProc(),
    }
    global_env = Environment(global_vars, global_funcs)

    @staticmethod
    def is_symbol_globally_bound(symbol: Symbol) -> bool:
        return BuiltIns.global_env.proc_bindings.get(symbol.value, None) is not None or \
            BuiltIns.global_env.var_bindings.get(symbol.value, None) is not None


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
            self.cons_q = []
            self.level = 0
            self.quote_q = []

        def empty(self):
            return len(self.cons_q) == 0

        def add(self, leaf):
            if len(self.cons_q) == 0:  # Not in any list
                return False
            root_cons, tar_cons = self.cons_q[-1]
            if tar_cons.car is None:  # (None . NIL)
                # Should only be reached on 1st call immediately after `open_list`
                tar_cons.car = leaf
            else:  # (x . NIL)
                assert tar_cons.cdr is BuiltIns.NIL
                tar_cons.cdr = Cons(car=leaf, cdr=BuiltIns.NIL)  # (x . (leaf . NIL))
                self.cons_q[-1] = root_cons, tar_cons.cdr
                if len(self.quote_q) > 0 and self.level == self.quote_q[-1]:
                    self.quote_q.pop()
                    self.close_list()
            return True

        def quote(self):
            self.open_list()
            self.add(Symbol('QUOTE'))
            self.quote_q.append(self.level)

        def open_list(self):
            self.level += 1
            cons = Cons(car=None, cdr=BuiltIns.NIL)
            self.cons_q.append((cons, cons))

        def close_list(self):
            self.level -= 1
            cons, _ = self.cons_q.pop()
            if cons.car is None:  # Empty list
                cons = BuiltIns.NIL
            if len(self.cons_q) == 0:
                return cons
            self.add(cons)

        def clear(self):
            self.cons_q.clear()
            self.level = 0
            self.quote_q.clear()

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
                    self.cons_builder.open_list()
                elif char == ')':
                    self.exit_atom_build()
                    try:
                        returned_list = self.cons_builder.close_list()
                    except IndexError:
                        raise Error.UnmatchedParenthesesException()
                    if returned_list is not None:
                        self.result.append(returned_list)
                elif char == '\'':
                    if self.symbol_build == '#':  # Rough fix
                        self.enter_atom_build(char)
                    else:
                        self.cons_builder.quote()

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
                atom = BuiltIns.String(self.symbol_build)
                self.string_building = False
            elif self.symbol_build.startswith("#'"):
                self.cons_builder.open_list()
                self.cons_builder.add(Symbol('FUNCTION'))
                self.symbol_build = self.symbol_build[2:]
                self.exit_atom_build()
                self.cons_builder.close_list()
                return
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
            self.symbol_build = ''


class CommonPyLispInterpreter:
    @staticmethod
    def run(code: str):
        run_env = Environment(*BuiltIns.global_env.copy())
        parser = Parser()
        parsed = parser.parse(code)
        for exp in parsed:
            exp.evaluate(run_env)


c = """
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

(print (quote (a b c)))
(print '(a b c))
(print (- 3 1 2))
"""

CommonPyLispInterpreter.run(c)
