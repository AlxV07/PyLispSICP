# Fermat's theorem
def exp_mod(base, exp, m):
    if exp == 0:
        return 1
    elif exp % 2 == 0:
        x = exp_mod(base, (exp / 2), m)
        return (x * x) % m
    else:
        return (base * exp_mod(base, exp - 1, m)) % m


def fermat_theorem(n):
    def run(a):
        return exp_mod(a, n, n) == a
    return run(n)
