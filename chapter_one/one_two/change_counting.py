# A function to count the number of ways to change an amount using an x amount of coins using tree recursion
def cc(amount, coin_kinds):
    if amount == 0:
        return 1
    elif coin_kinds == 0 or amount < 0:
        return 0
    else:
        return cc(amount, coin_kinds - 1) + cc(amount - get_count_amount(coin_kinds), coin_kinds)


def get_count_amount(x):
    if x == 1:
        return 1
    elif x == 2:
        return 5
    elif x == 3:
        return 10
    elif x == 4:
        return 25
    elif x == 5:
        return 50
