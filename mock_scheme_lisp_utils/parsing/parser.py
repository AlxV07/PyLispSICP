from mock_scheme_lisp_utils.lexing import tokens
import nodes


class Parser:
    def __init__(self):
        pass

    def parse(self, token_list):
        node_list = []

        level = 0
        exp_start = -1
        for i, token in enumerate(token_list):
            if isinstance(token, tokens.ExpStarter):
                if exp_start == -1:
                    exp_start = i
                level += 1
            elif isinstance(token, tokens.ExpEnder):
                level -= 1
                if level == 0:
                    exp_end = i
                    node = self.parse(token_list[exp_start + 1: exp_end])
                    # node_list.append(node)

        i = 0
        while i < len(token_list):
            token = token_list[i]
            if isinstance(token, tokens.ExpOperator):
                operands = []
                i += 1
                t = token_list[i]
                while isinstance(t, tokens.ExpOperand):
                    operands.append(t)
                    i += 1
                    t = token_list[i]
                node = nodes.Node(token.identifier, operands)
                node_list.append(node)

        return node_list
