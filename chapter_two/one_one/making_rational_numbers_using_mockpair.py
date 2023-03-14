from mock_scheme_lisp_pair import Pair, car, cdr


def make_rat(x, y):
    return Pair(x, y)


def numerator(z):
    return car(z)


def denominator(z):
    return cdr(z)


def print_rational_number(n):
    print(numerator(n), "/", denominator(n))
