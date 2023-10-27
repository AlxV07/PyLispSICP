class Token:
    def __init__(self):
        pass


class ExpStarter(Token):
    pass


class ExpEnder(Token):
    pass


class ExpIdentifier(Token):
    def __init__(self, identifier):
        super().__init__()
        self.identifier = identifier


class ExpOperator(ExpIdentifier):
    pass


class ExpOperand(ExpIdentifier):
    pass
