import math
from unittest import TestCase

from src.numericalsolution.main import solve


class Solve(TestCase):
    def test_wrong_bracket(self):
        assert solve(lambda x: x, 2, 1, 0.1, 0.1, "").is_ok is False

    def test_no_roots(self):
        assert solve(lambda x: x, 2, 3, 0.1, 0.1, "").is_ok is False


class Bisections(TestCase):
    def test_sinx_should_be_0(self):
        eps_x = 1e-6
        ans = solve(lambda x: math.sin(x), -1.1, 1, eps_x, eps_x, "bisections")
        self.assertAlmostEqual(ans.root, 0, 6)


class Chords(TestCase):
    def test_chords(self):
        assert solve(lambda x: x, -1, 1, 0.1, 0.1, "chords").root == 0

    def test_chords(self):
        eps_x = 1e-6
        ans = solve(lambda x: math.sin(x), -1.1, 1, eps_x, eps_x, "bisections")
        self.assertAlmostEqual(ans.root, 0, 6)


class Newton(TestCase):
    def test_newton(self):
        self.assertAlmostEqual(solve(lambda x: x * x + 2 * x - 3, -5, 0, 0.1, 0.1, "newton").root, -3, 1)

    def test_newton_small_eps(self):
        eps_x = 1e-6
        self.assertAlmostEqual(solve(lambda x: x * x + 2 * x - 3, -5, 0, eps_x, eps_x, "newton").root, -3, 10)


if __name__ == "__main__":
    TestCase
