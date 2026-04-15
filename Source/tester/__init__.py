import unittest  # pyright: ignore[reportImportCycles]

from . import (
    test_asset,
    test_logger,
    test_server,
    test_serialise,
)

NAMED_MODULES = {
    'serialise': test_serialise,
    'asset': test_asset,
    'logger': test_logger,
    'server': test_server,  # This goes last.
}

NAMED_SUITES = {
    name: unittest.TestLoader().loadTestsFromModule(module=module)
    for name, module in NAMED_MODULES.items()
}

DEFAULT_TEST_NAMES = list(NAMED_MODULES.keys())


def run_test(tests: list[str] = DEFAULT_TEST_NAMES) -> None:
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestSuite(
        suite
        for name in tests
        for suite in NAMED_SUITES.get(name, [])
    ))
