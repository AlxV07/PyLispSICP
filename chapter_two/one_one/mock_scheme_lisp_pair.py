def cons(x, y):
    def dispatch(m):
        if m == 0:
            return x
        elif m == 1:
            return y
        else:
            raise ValueError()

    return lambda p: dispatch(p)


def car(z):
    return z(0)


def cdr(z):
    return z(1)
