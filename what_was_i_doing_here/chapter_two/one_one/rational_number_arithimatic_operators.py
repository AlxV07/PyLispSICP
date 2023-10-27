from mock_scheme_lisp_pair import cons
from making_rational_numbers_using_mockpair import numerator, denominator


def add_rationals(x, y):
    return cons(
        (numerator(x) * denominator(y)) + (numerator(y) * denominator(x)),
        (denominator(x) * denominator(y))
    )


def sub_rationals(x, y):
    return cons(
        (numerator(x) * denominator(y)) - (numerator(y) * denominator(x)),
        (denominator(x) * denominator(y))
    )


def mul_rationals(x, y):
    return cons(
        (numerator(x) * numerator(y)),
        (denominator(x) * denominator(y))
    )


def div_rationals(x, y):
    return cons(
        (numerator(x) * denominator(y)),
        (denominator(x) * numerator(y))
    )


def rationals_equal(x, y):
    return numerator(x) * denominator(y) == numerator(y) * denominator(x)
