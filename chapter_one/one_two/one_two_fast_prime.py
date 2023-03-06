from one_two_fermat_theorem import fermat_theorem


def fast_prime(n, times):
    if times == 0:
        return True
    elif fermat_theorem(n):
        fast_prime(n, times - 1)
    else:
        return False
