def smallest_divisor(n):
    if n <= 1:
        return n - 1
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


# Optimized smallest_divisor
def better_smallest_divisor(n):
    if n <= 1:
        return n - 1
    else:
        return better_find_divisor(n, 2)


def better_find_divisor(n, divisor):
    if divisor * divisor > n:
        return n
    elif n % divisor == 0:
        return divisor
    else:
        return find_divisor(n, next_test_int(divisor))


def next_test_int(current_int):
    return 3 if current_int == 2 else current_int + 2
