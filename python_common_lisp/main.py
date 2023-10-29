from python_common_lisp.mock_lisp_interpreter import LispInterpreter

if __name__ == '__main__':
    interpreter = LispInterpreter()

    test_in = """
    (defun increment (a) (+ a 1))
    (increment 3)
    
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
    
    ((lambda (x y z) (+ x y (square z))) 1 2 3)
    
    (f (lambda (x) (+ x 3))) ;; COMMENT_TEST AWOOGA
    
    (defun cube (n) (* n n n))
    (defun bob () (if (= 1 0) square cube))
    (f (bob))
    f
    
    (defvar kk 4)
    kk
    
    (defun pow (n x)
        (if (= x 0)
            1
            (* n (pow n (- x 1)))
        )
    )
    (pow 3 3)
    (defvar a123 456)
    123
    a123
    789
    """
    result = interpreter.run(test_in)
    print(result)

    test_in = """
    (defun increment1 (n) (+ n 1)) 
    (increment (increment1 1))
    """
    result = interpreter.run(test_in)
    assert result == [3]

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
    assert result == [8]

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
                 fib
            """
    result = interpreter.run(test_in)
    assert result[0] == 2.0
