import math
from unittest import TestCase

from src.numericalsolution.DataWrapper.lambda_wrapper import LambdaWrapper
from src.numericalsolution.numerical_solver import NumericalSolver, brenth, methods, ridder
from tests.test_TupleArrayWrapper import TupleArrayWrapperFactory


class Solve(TestCase):
    def test_wrong_bracket(self):
        assert NumericalSolver.solve(LambdaWrapper(lambda x: x), "", 2, 1, 0.1, 0.1).is_ok is False

    def test_no_roots(self):
        assert NumericalSolver.solve(LambdaWrapper(lambda x: x), "", 2, 3, 0.1, 0.1).is_ok is False


class Bisections(TestCase):
    def test_sinx_should_be_0(self):
        eps_x = 1e-6
        ans = NumericalSolver.solve(LambdaWrapper(lambda x: math.sin(x)), "bisections", -1.1, 1, eps_x, eps_x)
        assert_ans(self, ans, 0)


class Chords(TestCase):
    def test_chords(self):
        assert NumericalSolver.solve(LambdaWrapper(lambda x: x), "bisections", -1, 1, 0.1, 0.1).root == 0

    def test_bisections(self):
        eps_x = 1e-6
        ans = NumericalSolver.solve(LambdaWrapper(lambda x: math.sin(x)), "bisections", -1.1, 1, eps_x, eps_x)
        assert_ans(self, ans, 0)


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
    self.assertAlmostEqual(ans.root, root, 6)
    self.assertTrue(ans.statistics.callsNumbers > 0)


if __name__ == "__main__":
    TestCase


class TestNumericalSolver(TestCase):

    def test_data_clear_statistics(self):
        taw = TupleArrayWrapperFactory.create_taw_1()
        k = NumericalSolver.solve_with_methods(taw.taw, taw.taw.get_min_x(), taw.taw.get_max_x(), methods, 1e-100,
                                               1e-100)

        summ = 0
        i = 0
        for ans in k.values():
            summ += ans.statistics.callsNumbers
            i += 1

        for ans in k.values():
            self.assertNotEqual(summ / i, ans.statistics.callsNumbers)

    def test_solve_from_tuples_1(self):
        taw = TupleArrayWrapperFactory.create_taw_1()
        k = NumericalSolver.solve_with_methods(taw.taw, taw.taw.get_min_x(), taw.taw.get_max_x(), methods, 1e-100,
                                               1e-100)
        self.assert_answer(k, taw)

    def test_solve_from_tuples_2(self):
        taw = TupleArrayWrapperFactory.create_taw_2()
        k = NumericalSolver.solve_with_methods(taw.taw, taw.taw.get_min_x(), taw.taw.get_max_x(), methods, 1e-100,
                                               1e-100)
        self.assert_answer(k, taw)

    def assert_answer(self, k, taw):
        for ans in k.values():
            self.assertEqual(taw.root, ans.root)
            if ans.method != ridder:
                self.assertEqual(True, ans.is_ok)


#     def test_solve_from_file_data(self):
#         k = NumericalSolver.solve_from_file_data("IgnoreFolder\\air_inlet.f.data")
#         file = open('IgnoreFolder\\myfile.dat', 'w+')
#         for resp in k:
#             file.write(f"{resp}\n")
#
#         file.close()
class TestNumericalSolverBrenth(TestCase):
    def test_brenth_solve_from_tuples(self):
        taw = TupleArrayWrapperFactory.create_taw_1()
        k = NumericalSolver.solve(taw.taw, brenth, taw.taw.get_min_x(), taw.taw.get_max_x(), 1e-100, 1e-100)
        assert_ans(self, k, taw.root)

        taw = TupleArrayWrapperFactory.create_taw_2()
        k = NumericalSolver.solve(taw.taw, brenth, taw.taw.get_min_x(), taw.taw.get_max_x(), 1e-100, 1e-100)
        assert_ans(self, k, taw.root)
