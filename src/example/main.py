from src.numericalsolution.numerical_solver import solve


def main():
    eps = 1e-5
    print("Solving x^2 + 2x + 3 = 0 with newton method on interval (-5, 5). (Should find no roots)")
    res = solve(lambda x: x * x + 2 * x + 3, -5, 5, eps, eps, 'newton')
    print_result(res)

    print("Solving x^2 + 2x - 3 = 0 with newton method on interval (-5, 0) (Should find root -3)")
    res = solve(lambda x: x * x + 2 * x - 3, -5, 0, eps, eps, 'newton')
    print_result(res)

    print("Solving x^2 + 2x - 3 = 0 with newton method on interval (0, 2) (Should find root 1)")
    res = solve(lambda x: x * x + 2 * x - 3, 0, 2, eps, eps, 'newton')
    print_result(res)

    print("Solving x^2 + 2x - 3 = 0 with bisection method on interval (0, 2) (Should find root 1 exactly)")
    res = solve(lambda x: x * x + 2 * x - 3, 0, 2, eps, eps, 'bisections')
    print_result(res)

    print("Solving x^2 + 2x - 3 = 0 with bisection method on interval (-0.1, 2) (Should find root '1')")
    res = solve(lambda x: x * x + 2 * x - 3, -0.1, 2, eps, eps, 'bisections')
    print_result(res)


def print_result(res):
    print(f'Result - Error occurred: {not res.is_ok}. Message: {res.message}')
    if res.is_ok:
        print(f'Root: {res.root}')

    print('')


if __name__ == "__main__":
    main()
