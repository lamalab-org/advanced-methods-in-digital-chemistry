"""Hand-calculable checks. Keep this file unchanged during the first repair."""

from math import isclose

from score import mean_squared_error


cases = [
    ("opposite residuals", [2, 0], [1, 1], 1.0),
    ("exact predictions", [0.2, 0.5], [0.2, 0.5], 0.0),
    ("unequal errors", [0, 3], [1, 1], 2.5),
]

failed = 0
for name, predictions, observations, expected in cases:
    actual = mean_squared_error(predictions, observations)
    passed = isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)
    print(f"{'PASS' if passed else 'FAIL'}: {name}: "
          f"expected {expected}, obtained {actual}")
    failed += not passed

raise SystemExit(1 if failed else 0)
