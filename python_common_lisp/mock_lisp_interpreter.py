class Atom:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Lexer:
    def __init__(self):
        self.result = []
        self.atom = ''

    def lex(self, code: str) -> list:
        code = ' '.join(map(lambda line: line if ';;' not in line else line[:line.index(';;')],
                            code.strip().split('\n')))
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
        self.exit_atom_build_state()
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
                return True
            return False

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
        for token in token_list:
            if token == '(':
                self.exp_queue.start_list()
            elif token == ')':
                r = self.exp_queue.end_list()
                if r is not None:
                    result.append(r)
            else:
                assert type(token) is Atom
                if not self.exp_queue.add(token):
                    result.append(token)
        if len(self.exp_queue.q) > 0: raise SyntaxError('Unclosed expression')
        return result


class Executor:
    class Pair:
        def __init__(self, car, cdr):
            self.car = car
            self.cdr = cdr

        def __str__(self):
            return f'Pair: ({self.car} . {self.cdr})'

    class Function:
        def __init__(self, name, parameters, expression):
            self.name = name
            self.parameters = parameters
            self.expression = expression

        def __str__(self):
            return f'Function: \'{self.name}\''

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

    def evaluate(self, obj, env: dict):
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
                        raise SyntaxError(f'Unknown: \'{obj.name}\'')

        elif type(obj) is Expression:
            operator = self.evaluate(obj.exp[0], env)
            operands = obj.exp[1:]
            if type(env.get(operator)) is self.Function:
                return self.defined_function(env[operator], operands, env)
            elif type(operator) is self.Function:  # Lambda
                return self.defined_function(operator, operands, env)
            else:
                if type(operator) is str: raise SyntaxError(f'Unknown operation: \'{operator}\'')
                return operator(operands, env)

        else:
            raise Exception(f'Unknown: \'{obj}\'')

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
            op = l.exp[0]
            try:
                self.evaluate(op, env)
                raise NameError(f'\'let\' : \'{op}\' illegal variable name')
            except SyntaxError:
                name = op.name
                val = self.evaluate(l.exp[1], env)
                env[name] = val
        return self.evaluate(operands[1], env)

    def defun(self, operands, env):
        if len(operands) != 3: raise SyntaxError(f'\'defun\' : Expected 3 arguments but received {len(operands)}')
        op = operands[0]
        try:
            self.evaluate(op, env)
            raise NameError(f'\'defun\' : \'{op}\' illegal function name')
        except SyntaxError:
            name = op.name
            env[name] = self.Function(name, operands[1].exp, operands[2])
        return None

    def defvar(self, operands, env):
        if len(operands) != 2: raise SyntaxError(f'\'defvar\' : Expected 2 arguments but received {len(operands)}')
        op = operands[0]
        try:
            self.evaluate(op, env)
            raise NameError(f'\'defvar\' : \'{op}\' illegal variable name')
        except SyntaxError:
            name = op.name
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
        return self.Pair(
            self.evaluate(operands[0], env),
            self.evaluate(operands[1], env)
        )

    def car(self, operands, env):
        if len(operands) != 1: raise SyntaxError(f'\'car\' : Expected 1 argument but received {len(operands)}')
        pair = self.evaluate(operands[0], env)
        if type(pair) is not self.Pair: raise SyntaxError(f'\'car\' : Expected argument of type \'Pair\''
                                                          f' but was \'{type(pair)}\'')
        return pair.car

    def cdr(self, operands, env):
        if len(operands) != 1: raise SyntaxError(f'\'cdr\' : Expected 1 argument but received {len(operands)}')
        pair = self.evaluate(operands[0], env)
        if type(pair) is not self.Pair: raise SyntaxError(f'\'cdr\' : Expected argument of type \'Pair\''
                                                          f' but was \'{type(pair)}\'')
        return pair.cdr

    def lambda_statement(self, operands, env):
        assert self, env
        if len(operands) != 2: raise SyntaxError(f'\'lambda\' : Expected 3 arguments but received {len(operands)}')
        return self.Function('lambda', operands[0].exp, operands[1])


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
            r = self.executor.evaluate(expression, self.executor.global_env)
            if r is not None:
                result.append(r)
        return result
