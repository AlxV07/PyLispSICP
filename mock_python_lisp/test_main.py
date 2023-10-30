from mock_python_lisp.mock_python_lisp_interpreter import LispInterpreter

if __name__ == '__main__':
    interpreter = LispInterpreter()

    test_in = """
    (defun abs (a)
        (if (> 0 a)
            (* a -1)
            a))
    (defun f (a) (a 2))
    (defun g (n) (+ n 2))
    (f g)
    """
    result = interpreter.run(test_in)
    print(result)

    test_in = """
    (defun increment1 (n) (+ n 1)) 
    (increment1 (increment1 1))
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
