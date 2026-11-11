"""Deterministic input-validation regression tests for the self-storage parser.

This complements the Hypothesis properties in test_processor.py. Execute with
python -m pytest -q test_validation_regression.py
"""

import math
import random
import string

import pytest

from processor import duration_average, parse_rental, payable_rent


@pytest.mark.parametrize("value", [
    None, "", "medium", ":5", "medium:", "medium:abc", "medium:-2",
    "medium:NaN", "medium:inf", "medium:2:extra", "::", "  :  ",
])
def test_parse_rental_rejects_invalid(value):
    assert parse_rental(value) is None


@pytest.mark.parametrize("value", [
    None, "", ",", "3,,6", "3,", "x,y", "-1,2", "3,2.5", "3|6", "  ",
])
def test_duration_average_rejects_invalid(value):
    assert duration_average(value) is None


@pytest.mark.parametrize("value", [
    None, "", "2400", "|200", "200|", "abc|2", "-1|5", "100|-1",
    "nan|2", "inf|0", "1.7e308|0", "2400|200|1", "  |  ",
])
def test_payable_rent_rejects_invalid(value):
    assert payable_rent(value) is None


def test_known_valid_examples():
    assert parse_rental("medium:6") == ("Medium", 6.0)
    assert duration_average("3,6,12") == 7
    assert payable_rent("2400|200") == pytest.approx(2632.0)
    assert payable_rent("100|200") == pytest.approx(0.0)


def test_seeded_valid_input_regressions():
    rng = random.Random(113)
    for _ in range(300):
        size = rng.choice(("small", "medium", "large"))
        months = rng.randrange(0, 2000)
        assert parse_rental(f"{size}:{months}") == (size.title(), float(months))
    for _ in range(300):
        values = [rng.randrange(0, 1000) for _ in range(rng.randrange(1, 30))]
        assert duration_average(",".join(map(str, values))) == sum(values) // len(values)
    for _ in range(300):
        rent = rng.randrange(0, 100000)
        discount = rng.randrange(0, 10000)
        assert payable_rent(f"{rent}|{discount}") == pytest.approx(max(rent * 1.18 - discount, 0.0))
