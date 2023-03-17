from chapter_two.one_one.mock_scheme_lisp_pair import cons, car, cdr

def mock_lisp_list(*args):
    return mock_lisp_list_backend(tuple(args))

def mock_lisp_list_backend(args):
    if len(args) == 1:
        return args[0]
    else:
        return cons(args[0], mock_lisp_list_backend(args[1:]))
