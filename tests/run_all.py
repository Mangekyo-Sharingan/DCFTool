"""
Test Runner for DCF Tool

Runs all unit tests and integration tests with coverage reporting.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_all_tests():
    """Run all tests with detailed output"""

    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*50}")
    print(f"TESTS RUN: {result.testsRun}")
    print(f"FAILURES: {len(result.failures)}")
    print(f"ERRORS: {len(result.errors)}")
    print(f"SKIPPED: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"{'='*50}")

    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)