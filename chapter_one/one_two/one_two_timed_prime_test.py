import time
from one_two_is_prime_formula import is_prime


def timed_prime_test(n):
    print(n)


def start_prime_test(n, start_time):
    if is_prime(n):
        report_prime(time.time() - start_time)


def report_prime(elapsed_time):
    print("***")
    print(elapsed_time)