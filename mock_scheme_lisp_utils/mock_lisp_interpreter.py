class Atom:
    def __init__(self, atom):
        self.atom = atom

    def evaluate(self, env: dict):
        if env.get(self.atom, None) is not None:
            return env[self.atom]
        else:
            try:
                return float(self.atom)
            except ValueError:
                return self.atom


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
        i = 0
        while i < len(token_list):
            token = token_list[i]
            if token == '(':
                self.exp_queue.start_list()
            elif token == ')':
                result = self.exp_queue.end_list()
                if result is not None:
                    return result
            else:
                self.exp_queue.add(token)
            i += 1
        raise SyntaxError


class Executor:
    def __init__(self):
        self.global_env = {
            '+': self.add,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,

            'let': self.let,
            'defun': None,

        }

    def evaluate(self, obj, env: dict = None):
        if env is None:
            env = self.global_env
        if type(obj) is Atom:
            return obj.evaluate(env)
        elif type(obj) is List:
            operator = self.evaluate(obj.exp[0], env)
            operands = obj.exp[1:]
            return operator(operands, env)
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
