from unittest import TestCase

from src.numericalsolution.DataWrapper.lambda_wrapper import LambdaWrapper


class TestLambdaWrapper(TestCase):
    def test_get_value_at(self):
        k = LambdaWrapper(lambda x: x*x)
        for i in range(0, 20):
            self.assertEqual(k.get_value_at(i), i*i)

    def test_get_value_by_call(self):
        k = LambdaWrapper(lambda x: x * x)
        for i in range(0, 20):
            self.assertEqual(k(i), i * i)

