from mock_scheme_lisp_utils.mock_lisp_interpreter import LispInterpreter

if __name__ == '__main__':
    interpreter = LispInterpreter()

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
