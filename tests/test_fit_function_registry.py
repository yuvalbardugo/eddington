from unittest import TestCase

from eddington_core import (
    FitFunctionLoadError,
    FitFunctionsRegistry,
    fit_function,
)
from eddington_core.exceptions import FitFunctionSaveError


class TestFitFunctionRegistryAddAndRemove(TestCase):
    def setUp(self):
        self.backup = list(FitFunctionsRegistry.all())
        FitFunctionsRegistry.clear()
        self.func1 = self.dummy_function(1)
        self.func2 = self.dummy_function(2)
        self.func3 = self.dummy_function(3)
        self.func4 = self.dummy_function(4, save=False)

        self.funcs = [self.func1, self.func2, self.func3]

    def tearDown(self):
        FitFunctionsRegistry.clear()
        for func in self.backup:
            FitFunctionsRegistry.add(func)

    @classmethod
    def dummy_function(cls, value, save=True):
        @fit_function(
            n=2,
            name=f"dummy_function{value}",
            syntax=f"syntax_dummy_function{value}",
            save=save,
        )
        def dummy_func(a, x):  # pylint: disable=W0613
            return value

        return dummy_func

    def test_load_function(self):
        actual_func = FitFunctionsRegistry.load(self.func1.name)
        self.assertEqual(
            self.func1,
            actual_func,
            msg="Registry get name function returns different function than expected.",
        )

    def test_exists(self):
        for func in self.funcs:
            self.assertTrue(
                FitFunctionsRegistry.exists(func.name),
                msg=f"Expected {func.name} to exists. It does not.",
            )

    def test_remove(self):
        FitFunctionsRegistry.remove(self.func1.name)
        self.assertFalse(
            FitFunctionsRegistry.exists(self.func1.name),
            msg=f"Expected {self.func1.name} to not exist. It does.",
        )

    def test_all(self):
        self.assertEqual(
            self.funcs,
            list(FitFunctionsRegistry.all()),
            msg="Functions are different than expected",
        )

    def test_names(self):
        self.assertEqual(
            [func.name for func in self.funcs],
            list(FitFunctionsRegistry.names()),
            msg="Functions names are different than expected",
        )

    def test_syntax_of_one_function(self):
        syntax = FitFunctionsRegistry.syntax([self.func1.name])
        expected_string = """
+-----------------+------------------------+
|     Function    |         Syntax         |
+-----------------+------------------------+
| dummy_function1 | syntax_dummy_function1 |
+-----------------+------------------------+"""
        self.assertEqual(
            expected_string[1:],
            str(syntax),
            msg="Syntax of one function is different than expected.",
        )

    def test_syntax_of_two_functions(self):
        syntax = FitFunctionsRegistry.syntax([self.func1.name, self.func3.name])
        expected_string = """
+-----------------+------------------------+
|     Function    |         Syntax         |
+-----------------+------------------------+
| dummy_function1 | syntax_dummy_function1 |
| dummy_function3 | syntax_dummy_function3 |
+-----------------+------------------------+"""
        self.assertEqual(
            expected_string[1:],
            str(syntax),
            msg="Syntax of two functions is different than expected.",
        )

    def test_list(self):
        syntax = FitFunctionsRegistry.list()
        expected_string = """
+-----------------+------------------------+
|     Function    |         Syntax         |
+-----------------+------------------------+
| dummy_function1 | syntax_dummy_function1 |
| dummy_function2 | syntax_dummy_function2 |
| dummy_function3 | syntax_dummy_function3 |
+-----------------+------------------------+"""
        self.assertEqual(
            expected_string.strip(),
            str(syntax).strip(),
            msg="Syntax of two functions is different than expected.",
        )

    def test_add_dummy_function_without_saving(self):
        self.assertFalse(
            FitFunctionsRegistry.exists(self.func4.name),
            msg="Function was saved, even though it wasn't supposed to",
        )

    def test_load_non_existing_function(self):
        self.assertRaisesRegex(
            FitFunctionLoadError,
            f"^No fit function named {self.func4.name}$",
            FitFunctionsRegistry.load,
            self.func4.name,
        )

    def test_saving_two_fit_functions_with_the_same_name(self):
        self.assertRaisesRegex(
            FitFunctionSaveError,
            '^Cannot save "dummy_function2" to registry '
            "since there is another fit function with this name$",
            self.dummy_function,
            value=2,
            save=True,
        )

