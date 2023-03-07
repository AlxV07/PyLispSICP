# A method to time how fast it takes to calculate whether a number is prime;
# comparing the methods fast_prime and is_prime
import time

from chapter_one.one_two.fast_prime import fast_prime
from is_prime_formula import is_prime


def timed_prime_test(n):
    start_prime_test(n, time.time())


def start_prime_test(n, start_time):
    if is_prime(n):
        print(n)
        report_prime(time.time() - start_time)


def report_prime(elapsed_time):
    print(elapsed_time)
    print("***")


# Timed prime test using fast_prime
def timed_fast_prime_test(n):
    start_fast_prime_test(n, time.time())


def start_fast_prime_test(n, start_time):
    if fast_prime(n, int(n * 0.7)):
        print(n)
        report_prime(time.time() - start_time)
