# Formula to find the Greatest Common Divisor of two numbers x and y
def gcd(x, y):
    if y == 0:
        return x
    else:
        return gcd(y, x % y)


print(gcd(24, 12))
