from unittest import TestCase
from tests.fit_function.dummy_functions import dummy_func1
from tests.fit_function.fit_function_base_test_case import FitFunctionBaseTestCase


class TestSimpleFitFunction(FitFunctionBaseTestCase, TestCase):
    func = dummy_func1
    n = 2
    values = [
        ([2, 1], 3, 11),
        ([-2.1, 4], 0.6, -0.66),
        ([4, -0.5], 3, -0.5),
        ([9, 2], 0, 9),
    ]


class TestFitFunctionNegative(FitFunctionBaseTestCase, TestCase):
    func = -dummy_func1
    n = 2
    values = [
        ([2, 1], 3, -11),
        ([-2.1, 4], 0.6, 0.66),
        ([4, -0.5], 3, 0.5),
        ([9, 2], 0, -9),
    ]


class TestFitFunctionAddNumberFromRight(FitFunctionBaseTestCase, TestCase):
    func = dummy_func1 + 5.2
    n = 2
    values = [
        ([2, 1], 3, 16.2),
        ([-2.1, 4], 0.6, 4.54),
        ([4, -0.5], 3, 4.7),
        ([9, 2], 0, 14.2),
    ]