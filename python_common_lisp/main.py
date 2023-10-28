from python_common_lisp.mock_lisp_interpreter import LispInterpreter

if __name__ == '__main__':
    interpreter = LispInterpreter()

    test_in = """
    (let ((x 1) (y 2) (z 3)) (+ x y z))
    (defun p (a b) (+ a b))
    (p 1 2)
    
    (let ((x 1))
        (p (p x x) (p x x) )
    )
    
    (= 1 1)
    
    (defun max (x y) (if (> x y) x y))
    (max 3 10.0)
    
    (and true false false)
    (and true true true)
    (not (or false false false (and false true) (and true true)))
    (or false false false)
    
    (let ((x (cons 1 2)))
        (cdr x)
    )
    
    (defun to () (cons 1 2))
    (car (to))
    (cdr (to))
    
    (defvar acon (cons (cons 1 2) (cons 3 4)))
    (car (car acon))
    (cdr (car acon))
    (car (cdr acon))
    (cdr (cdr acon))
    
    (defun square (n) (* n n))
    (defun f (g) (g 2))
    (f square)
    (f (lambda (x) (+ x 3)))
    ((lambda (x y z) (+ x y (square z))) 1 2 3)
    
    (defun cube (n) (* n n n))
    (defun bob () (if (> 1 0) square cube))
    (f (bob))
    """
    result = interpreter.run(test_in)
    print(result)

    test_in = """
    (defun increment (n) (+ n 1)) 
    (increment (increment 1))
    """
    result = interpreter.run(test_in)
    assert result == [None, 3]

    test_in = """
    (defun fib (n)
        (if (< n 2)
            n
            (+
                (fib (- n 1))
                (fib (- n 2))
            )
        )
    )
    (fib 6)
    """
    result = interpreter.run(test_in)
    assert result == [None, 8]

    test_in = """(+
    1
    (+ 2 3) 
    (+ 2 2)
    (+ 5 2 3 10)
    (+ 2 (+ 1 3 (+ 1 3)))
    )
    """
    result = interpreter.run(test_in)[0]
    assert result == 40.0

    test_in = """(+
        10 20 (- 0 5 3 2)
        )
        """
    result = interpreter.run(test_in)[0]
    assert result == 20.0

    test_in = """(* 12 5 4)
    """
    result = interpreter.run(test_in)[0]
    assert result == 240.0

    test_in = """(/ 72 3)
        """
    result = interpreter.run(test_in)[0]
    assert result == 24.0

    test_in = """(let ((x 1) (y 1)) 
                    (+ x y))
            """
    result = interpreter.run(test_in)[0]
    assert result == 2.0
