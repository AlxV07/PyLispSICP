from one_two_timed_prime_test import timed_prime_test


def search_for_primes(begin, end):
    for i in range(begin, end):
        if i != 2 and i % 2 == 0:
            i += 1
        else:
            timed_prime_test(i)


search_for_primes(1000, 2000)
