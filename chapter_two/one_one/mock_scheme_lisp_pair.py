class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dispatch(self, m):
        if m == 0:
            return self.x
        elif m == 1:
            return self.y
        else:
            raise Exception()

    def __str__(self):
        return "{0}, {1}".format(self.x, self.y)


def cons(x, y):
    return Pair(x, y)


def car(z):
    if type(z) == Pair:
        return z.dispatch(0)
    else:
        return z


def cdr(z):
    if type(z) == Pair:
        return z.dispatch(1)
    else:
        return None
