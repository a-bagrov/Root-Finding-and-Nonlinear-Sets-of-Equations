def derivative(f, x):
    delta = 1e-5
    return (f(x + delta) - f(x)) / delta
