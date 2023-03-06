import time
from one_two_is_prime_formula import is_prime


def timed_prime_test(n):
    start_prime_test(n, time.time())


def start_prime_test(n, start_time):
    if is_prime(n):
        print(n)
        report_prime(time.time() - start_time)


def report_prime(elapsed_time):
    print(elapsed_time)
    print("***")
