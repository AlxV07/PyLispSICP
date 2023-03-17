from chapter_two.one_one.mock_scheme_lisp_pair import cons, car, cdr

a = cons(1, 2)
b = cons(3, 4)
c = cons(a, b)

a1 = cons(1, cons(2, cons(3, cons(4, None))))

print(car(car(c)))
print(cdr(car(c)))
print(car(cdr(c)))
print(cdr(cdr(c)))

print(car(cdr(cdr(cdr(a1)))))
