# A linear iterative formula to print the layers of the pascal triangle
def pascal_iter(current_level, max_level, data):
    if len(data) == 0:
        x = [1]
    else:
        x = [0 for _ in range(len(data) + 1)]
        for i in range(len(data)):
            x[i] += data[i]
            x[i+1] += data[i]
    print(x)
    if current_level < max_level:
        pascal_iter(current_level+1, max_level, x)


def pascal_formula(level):
    pascal_iter(1, level, [])


pascal_formula(7)
