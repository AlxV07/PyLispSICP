from tokens import *


class Lexer:
    def __init__(self):
        self.result = None
        self.identifier = ''

    def lex(self, code: str):
        code = code.replace('\n', ' ').replace('  ', ' ').strip()

        self.result = []
        for char in code:
            if char == ' ':
                self.exit_identifier_state()
            elif char == '(':
                self.exit_identifier_state()
                self.result.append(ExpStarter())
            elif char == ')':
                self.exit_identifier_state()
                self.result.append(ExpEnder())
            else:
                self.identifier += char
        return self.result

    def exit_identifier_state(self):
        if len(self.identifier) > 0:
            if isinstance(self.result[-1], ExpStarter):
                token = ExpOperator
            else:
                token = ExpOperand
            self.result.append(token(self.identifier))
            self.identifier = ''


test_in = """(+ 1
(+ 2 3)
)
"""
print(Lexer().lex(test_in))
