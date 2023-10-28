class Atom:
    def __init__(self, name):
        self.name = name


class Lexer:
    def __init__(self):
        self.result = []
        self.atom = ''

    def lex(self, code: str) -> list:
        code = code.replace('\n', ' ').replace('  ', ' ').strip()
        self.result.clear()
        for char in code:
            if char == ' ':
                self.exit_atom_build_state()
            elif char == '(':
                self.exit_atom_build_state()
                self.result.append('(')
            elif char == ')':
                self.exit_atom_build_state()
                self.result.append(')')
            else:
                self.atom += char
        return self.result

    def exit_atom_build_state(self):
        if len(self.atom) > 0:
            token = Atom(self.atom)
            self.result.append(token)
            self.atom = ''


class Expression:
    def __init__(self):
        self.exp = []

    def add(self, token):
        self.exp.append(token)


class Parser:
    class ExpressionQueue:
        def __init__(self):
            self.q = []

        def clear(self):
            self.q.clear()

        def add(self, atom):
            if len(self.q) > 0:
                self.q[-1].add(atom)

        def start_list(self):
            self.q.append(Expression())

        def end_list(self):
            exp = self.q.pop()
            if len(self.q) > 0:
                self.q[-1].add(exp)
            else:
                return exp

    def __init__(self):
        self.exp_queue = self.ExpressionQueue()

    def parse(self, token_list: list):
        self.exp_queue.clear()
        result = []
        i = 0
        while i < len(token_list):
            token = token_list[i]
            if token == '(':
                self.exp_queue.start_list()
            elif token == ')':
                r = self.exp_queue.end_list()
                if r is not None:
                    result.append(r)
            else:
                self.exp_queue.add(token)
            i += 1
        return result


class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr


class Function:
    def __init__(self, parameters, expression):
        self.parameters = parameters
        self.expression = expression


class Executor:
    def __init__(self):
        self.global_env = {
            '+': self.add,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,

            'let': self.let,
            'defun': self.defun,
            'defvar': self.defvar,
            'lambda': self.lambda_statement,

            'if': self.if_statement,
            '<': self.greater_than,
            '>': self.less_than,
            '=': self.equal_to,
            'not': self.not_statement,
            'and': self.and_statement,
            'or': self.or_statement,
            'true': True,
            'false': False,

            'cons': self.cons,
            'car': self.car,
            'cdr': self.cdr,
        }

    def evaluate(self, obj, env: dict = None):
        if env is None:
            env = self.global_env

        if type(obj) is Atom:
            if env.get(obj.name, None) is not None:
                return env[obj.name]
            else:
                try:
                    return int(obj.name)
                except ValueError:
                    try:
                        return float(obj.name)
                    except ValueError:
                        return obj.name

        elif type(obj) is Expression:
            operator = self.evaluate(obj.exp[0])
            operands = obj.exp[1:]
            if type(env.get(operator)) is Function:
                return self.defined_function(env[operator], operands, env)
            elif type(operator) is Function:  # Lambda
                return self.defined_function(operator, operands, env)
            else:
                operator = self.evaluate(operator, env)
                if type(operator) is str: raise SyntaxError(f'Unknown operation: \'{operator}\'')
                return operator(operands, env)

        else:
            return obj

    def add(self, operands, env):
        if len(operands) < 2: raise SyntaxError(f'\'+\' : Expected >=2 arguments but received {len(operands)}')
        return sum(map(lambda o: self.evaluate(o, env), operands))

    def minus(self, operands, env):
        if len(operands) < 2: raise SyntaxError(f'\'-\' : Expected >=2 arguments but received {len(operands)}')
        total = self.evaluate(operands[0], env)
        for op in operands[1:]:
            total -= self.evaluate(op, env)
        return total

    def multiply(self, operands, env):
        if len(operands) < 2: raise SyntaxError(f'\'*\' : Expected >=2 arguments but received {len(operands)}')
        total = self.evaluate(operands[0], env)
        for op in operands[1:]:
            total *= self.evaluate(op, env)
        return total

    def divide(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'/\' : Expected 2 arguments but received {len(operands)}')
        return self.evaluate(operands[0], env) / self.evaluate(operands[1], env)

    def let(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'let\' : Expected 2 arguments but received {len(operands)}')
        env = env.copy()
        for l in operands[0].exp:
            name = self.evaluate(l.exp[0], env)
            if type(name) is not str: raise SyntaxError(f'\'let\' : \'{l.exp[0]}\' is already defined')
            val = self.evaluate(l.exp[1], env)
            env[name] = val
        return self.evaluate(operands[1], env)

    def defun(self, operands, env):
        if len(operands) != 3: raise SyntaxError(f'\'defun\' : Expected 3 arguments but received {len(operands)}')
        name = self.evaluate(operands[0], env)
        if type(name) is not str: raise SyntaxError(f'\'defun\' : \'{operands[0]}\' is already defined')
        env[name] = Function(operands[1].exp, operands[2])
        return None

    def defvar(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'defvar\' : Expected 2 arguments but received {len(operands)}')
        name = self.evaluate(operands[0], env)
        if type(name) is not str: raise SyntaxError(f'\'defvar\' : \'{operands[0]}\' is already defined')
        env[name] = self.evaluate(operands[1], env)
        return None

    def defined_function(self, func, operands, env):
        parameters, expression = func.parameters, func.expression
        if len(parameters) != len(operands):
            raise SyntaxError(f'\'{func}\' : Expected {len(parameters)} argument{"" if len(parameters) == 1 else "s"}'
                              f' but received {len(operands)}')
        env = env.copy()
        for parameter, operand in zip(parameters, operands):
            env[parameter.name] = self.evaluate(operand, env)
        return self.evaluate(expression, env)

    def if_statement(self, operands, env):
        if len(operands) != 3: raise SyntaxError(f'\'if\' : Expected 3 arguments but received {len(operands)}')
        condition = self.evaluate(operands[0], env)
        if condition:
            return self.evaluate(operands[1], env)
        else:
            return self.evaluate(operands[2], env)

    def not_statement(self, operands, env):
        if len(operands) != 1: raise SyntaxError(f'\'not\' : Expected 1 argument but received {len(operands)}')
        return not self.evaluate(operands[0], env)

    def and_statement(self, operands, env):
        for operand in operands:
            if not self.evaluate(operand, env):
                return False
        return True

    def or_statement(self, operands, env):
        for operand in operands:
            if self.evaluate(operand, env):
                return True
        return False

    def greater_than(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'<\' : Expected 2 arguments but received {len(operands)}')
        return self.evaluate(operands[0], env) < self.evaluate(operands[1], env)

    def less_than(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'>\' : Expected 2 arguments but received {len(operands)}')
        return self.evaluate(operands[0], env) > self.evaluate(operands[1], env)

    def equal_to(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'=\' : Expected 2 arguments but received {len(operands)}')
        return self.evaluate(operands[0], env) == self.evaluate(operands[1], env)

    def cons(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'cons\' : Expected 2 arguments but received {len(operands)}')
        return Pair(
            self.evaluate(operands[0], env),
            self.evaluate(operands[1], env)
        )

    def car(self, operands, env):
        if len(operands) != 1: raise SyntaxError(f'\'car\' : Expected 1 argument but received {len(operands)}')
        pair = self.evaluate(operands[0], env)
        if type(pair) is not Pair: raise SyntaxError(f'\'car\' : Expected argument of type \'Pair\''
                                                     f' but was \'{type(pair)}\'')
        return pair.car

    def cdr(self, operands, env):
        if len(operands) != 1: raise SyntaxError(f'\'cdr\' : Expected 1 argument but received {len(operands)}')
        pair = self.evaluate(operands[0], env)
        if type(pair) is not Pair: raise SyntaxError(f'\'cdr\' : Expected argument of type \'Pair\''
                                                     f' but was \'{type(pair)}\'')
        return pair.cdr

    def lambda_statement(self, operands, env):
        assert self, env
        if len(operands) != 2: raise SyntaxError(f'\'lambda\' : Expected 3 arguments but received {len(operands)}')
        return Function(operands[0].exp, operands[1])


class LispInterpreter:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.executor = Executor()

    def run(self, code: str):
        token_list = self.lexer.lex(code)
        expressions = self.parser.parse(token_list)
        result = []
        for expression in expressions:
            result.append(self.executor.evaluate(expression))
        return result
