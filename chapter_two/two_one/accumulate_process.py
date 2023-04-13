from chapter_two.one_one.mock_scheme_lisp_pair import cdr, car


def accumulate(operator, initial, sequence):
    if sequence is None:
        return initial
    else:
        return operator(car(sequence), accumulate(operator, initial, cdr(sequence)))
