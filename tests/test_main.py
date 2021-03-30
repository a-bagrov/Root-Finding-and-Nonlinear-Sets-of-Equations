import math
from unittest import TestCase

from src.numericalsolution.numerical_solver import NumericalSolver
from src.numericalsolution.DataWrapper.lambda_wrapper import LambdaWrapper
from src.numericalsolution.DataWrapper.tuple_array_wrapper import TupleArrayWrapper
import pandas as pd


class Solve(TestCase):
    def test_wrong_bracket(self):
        assert NumericalSolver.solve(LambdaWrapper(lambda x: x), "", 2, 1, 0.1, 0.1).is_ok is False

    def test_no_roots(self):
        assert NumericalSolver.solve(LambdaWrapper(lambda x: x), "", 2, 3, 0.1, 0.1).is_ok is False


class Bisections(TestCase):
    def test_sinx_should_be_0(self):
        eps_x = 1e-6
        ans = NumericalSolver.solve(LambdaWrapper(lambda x: math.sin(x)), "bisections", -1.1, 1, eps_x, eps_x)
        assert_ans(self, ans, 6)


class Chords(TestCase):
    def test_chords(self):
        assert NumericalSolver.solve(LambdaWrapper(lambda x: x), "bisections", -1, 1, 0.1, 0.1).root == 0

    def test_bisections(self):
        eps_x = 1e-6
        ans = NumericalSolver.solve(LambdaWrapper(lambda x: math.sin(x)), "bisections", -1.1, 1, eps_x, eps_x)
        assert_ans(self, ans, 6)


class Newton(TestCase):
    def test_newton(self):
        self.assertAlmostEqual(
            NumericalSolver.solve(LambdaWrapper(lambda x: x * x + 2 * x - 3), "newton", -5, 0, 0.1, 0.1).root, -3, 1)

    def test_newton_small_eps(self):
        eps_x = 1e-6
        self.assertAlmostEqual(
            NumericalSolver.solve(LambdaWrapper(lambda x: x * x + 2 * x - 3), "newton", -5, 0, eps_x, eps_x).root, -3,
            10)


def assert_ans(self, ans, root):
    self.assertTrue(ans.is_ok)
    self.assertAlmostEqual(ans.root, 0, root)
    self.assertTrue(ans.statistics.callsNumbers > 0)


if __name__ == "__main__":
    TestCase
