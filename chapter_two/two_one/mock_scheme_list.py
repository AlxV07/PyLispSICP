from chapter_two.one_one.mock_scheme_lisp_pair import cons, car, cdr, Pair

def mock_lisp_list(*args):
    return mock_lisp_list_backend(tuple(args))

def mock_lisp_list_backend(args):
    if len(args) == 1:
        return args[0]
    else:
        return cons(args[0], mock_lisp_list_backend(args[1:]))

def mock_lisp_list_ref(i, n):
    if type(i) != Pair:
        return i
    elif n == 0:
        return car(i)
    else:
        return mock_lisp_list_ref(cdr(i), n - 1)

def mock_lisp_list_length(i):
    pass
    if i is None:
        return 0
    elif type(i) != Pair:
        return 1
    else:
        return 1 + mock_lisp_list_length(cdr(i))
