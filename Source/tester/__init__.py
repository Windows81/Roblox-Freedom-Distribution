import unittest

from . import (
    test_asset,
    test_hotpatch,
)

NAMED_MODULES = {
    'asset': test_asset,
    'hotpatch': test_hotpatch,
}

NAMED_SUITES = {
    name: unittest.TestLoader().loadTestsFromModule(test)
    for name, test in NAMED_MODULES.items()
}

DEFAULT_TEST_NAMES = set(NAMED_MODULES.keys())


def run_test(tests: set[str] = DEFAULT_TEST_NAMES):
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestSuite(
        suite
        for name in tests
        for suite in NAMED_SUITES[name]
    ))
