def smallest_divisor(n):
    if n <= 1:
        return n-1
    else:
        return find_divisor(n, 2)


def find_divisor(n, divisor):
    if divisor * divisor > n:
        return n
    elif n % divisor == 0:
        return divisor
    else:
        return find_divisor(n, divisor + 1)


def is_prime(n):
    return n == smallest_divisor(n)
