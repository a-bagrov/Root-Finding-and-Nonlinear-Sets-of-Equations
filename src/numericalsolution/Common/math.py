DELTA_X_DERIVATE = 1e-5


def derivative(f, x, delta_x):
    return (f.get_value_at(x + delta_x) - f.get_value_at(x)) / delta_x
