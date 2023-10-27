from mock_scheme_lisp_utils.mock_lisp_interpreter import Lexer, Parser, Executor

if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    test_in = """(+
    1
    (+ 2 3) 
    (+ 2 2)
    (+ 5 2 3 10)
    (+ 2 (+ 1 3 (+ 1 3)))
    )
    """
    token_list = lexer.lex(test_in)
    print(token_list)
    expression = parser.parse(token_list)
    print(expression)
    # result = executor.evaluate(expression)
    # print(result)
    # assert result == 40.0
    print()

    test_in = """(+
        10 20 (- 0 5 3 2)
        )
        """
    token_list = lexer.lex(test_in)
    print(token_list)
    expression = parser.parse(token_list)
    print(expression)
    # result = executor.evaluate(expression)
    # print(result)
    # assert result == 20.0
    print()

    test_in = """(* 12 5 4)
    """
    token_list = lexer.lex(test_in)
    print(token_list)
    expression = parser.parse(token_list)
    print(expression)
    # result = executor.evaluate(expression)
    # print(result)
    # assert result == 240.0
    print()

    test_in = """(/ 72 3)
        """
    token_list = lexer.lex(test_in)
    print(token_list)
    expression = parser.parse(token_list)
    print(expression)
    # result = executor.evaluate(expression)
    # print(result)
    # assert result == 24.0
    print()

    test_in = """(let ((x 1) (y 1)) 
                    (+ x y))
            """
    token_list = lexer.lex(test_in)
    print(token_list)
    expression = parser.parse(token_list)
    print(expression)
    print(expression.exp)
    result = executor.evaluate(expression)
    print(result)
    assert result == 2.0
