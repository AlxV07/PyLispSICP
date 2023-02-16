def sqrt(x):
    def good_enough(guess, x) -> bool:
        return abs(x - (guess * guess)) < 0.001

    def improve_guess(guess, x):
        return (guess + (x / guess)) / 2

    def sqrt_iter(guess, x):
        return guess if good_enough(guess, x) else sqrt_iter(improve_guess(guess, x), x)

    return sqrt_iter(1, x)


print(sqrt(4))
print(sqrt(16))
print(sqrt(36))
