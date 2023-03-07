# Fibonacci formula using linear iteration
def better_fib(n):
    return better_fib_iter(1, 0, n)


def better_fib_iter(a, b, count):
    if count == 0:
        return b
    else:
        return better_fib_iter(a + b, a, count - 1)

