from chapter_two.one_one.mock_scheme_lisp_pair import cons, car, cdr


def mock_scheme_lisp_map(procedure, items):
    if items is None:
        return None
    else:
        return cons(procedure(car(items)), mock_scheme_lisp_map(procedure, cdr(items)))