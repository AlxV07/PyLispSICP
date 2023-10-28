class Atom:
    def __init__(self, name):
        self.name = name

    def evaluate(self, env: dict):
        if env.get(self.name, None) is not None:
            return env[self.name]
        else:
            try:
                return int(self.name)
            except ValueError:
                try:
                    return float(self.name)
                except ValueError:
                    return self.name


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


class List:
    def __init__(self):
        self.exp = []

    def add(self, token):
        self.exp.append(token)


class Parser:
    class ListQueue:
        def __init__(self):
            self.q = []

        def clear(self):
            self.q.clear()

        def add(self, atom):
            if len(self.q) > 0:
                self.q[-1].add(atom)

        def start_list(self):
            self.q.append(List())

        def end_list(self):
            exp = self.q.pop()
            if len(self.q) > 0:
                self.q[-1].add(exp)
            else:
                return exp

    def __init__(self):
        self.exp_queue = self.ListQueue()

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


class Executor:
    def __init__(self):
        self.global_env = {
            '+': self.add,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,

            'let': self.let,
            'defun': self.defun,

            'if': self.if_statement,
            '<': self.greater_than,
            '>': self.less_than,
        }

    def evaluate(self, obj, env: dict = None):
        if env is None:
            env = self.global_env
        if type(obj) is Atom:
            return obj.evaluate(env)
        elif type(obj) is List:
            operator_atom = obj.exp[0]
            operands = obj.exp[1:]
            if type(env.get(operator_atom.name)) is tuple:  # Is a user_defined_func
                return self.user_defined_func(operator_atom.name, operands, env)
            else:
                operator = self.evaluate(operator_atom, env)
                try:
                    return operator(operands, env)
                except TypeError:
                    raise SyntaxError
        else:
            return obj

    def add(self, operands, env):
        if len(operands) < 2: raise SyntaxError
        return sum(map(lambda o: self.evaluate(o, env), operands))

    def minus(self, operands, env):
        if len(operands) < 2: raise SyntaxError
        total = self.evaluate(operands[0], env)
        for op in operands[1:]:
            total -= self.evaluate(op, env)
        return total

    def multiply(self, operands, env):
        if len(operands) < 2: raise SyntaxError
        total = self.evaluate(operands[0], env)
        for op in operands[1:]:
            total *= self.evaluate(op, env)
        return total

    def divide(self, operands, env):
        if len(operands) != 2: raise SyntaxError
        return self.evaluate(operands[0], env) / self.evaluate(operands[1], env)

    def let(self, operands, env):
        if len(operands) != 2: raise SyntaxError
        env = env.copy()
        for l in operands[0].exp:
            name = l.exp[0].evaluate(env)
            assert type(name) is str
            val = self.evaluate(l.exp[1], env)
            env[name] = val
        return self.evaluate(operands[1], env)

    def defun(self, operands, env):
        assert self.user_defined_func is not None
        if len(operands) != 3: raise SyntaxError
        name = operands[0].evaluate(env)
        assert type(name) is str
        env[name] = (operands[1].exp, operands[2])  # parameters: list, List: List
        return None

    def user_defined_func(self, name: str, operands: list, env: dict):
        parameters, expression = env[name]
        assert len(parameters) == len(operands)
        env = env.copy()
        for par, val in zip(parameters, operands):
            env[par.name] = self.evaluate(val, env)
        return self.evaluate(expression, env)

    def if_statement(self, operands, env):
        if len(operands) != 3: raise SyntaxError
        condition = self.evaluate(operands[0], env)
        if condition:
            return self.evaluate(operands[1], env)
        else:
            return self.evaluate(operands[2], env)

    def greater_than(self, operands, env):
        if len(operands) != 2: raise SyntaxError
        return self.evaluate(operands[0], env) < self.evaluate(operands[1], env)

    def less_than(self, operands, env):
        if len(operands) != 2: raise SyntaxError
        return self.evaluate(operands[0], env) > self.evaluate(operands[1], env)


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
