from importlib import import_module
import unittest
import pathlib

NAMED_MODULES = {
    f.stem.lower(): import_module(f".{f.stem}", __package__)
    for f in pathlib.Path(__file__).parent.glob("test_*.py")
    if "__" not in f.stem
}

suite = unittest.TestSuite()
NAMED_SUITES = {
    name: unittest.TestLoader().loadTestsFromModule(test)
    for name, test in NAMED_MODULES.items()
}

DEFAULT_TEST_NAMES = set(NAMED_MODULES.keys())


def run_test(tests: set[str] = DEFAULT_TEST_NAMES):
    runner = unittest.TextTestRunner()
    for name, suite in NAMED_SUITES.items():
        runner.run(suite)
