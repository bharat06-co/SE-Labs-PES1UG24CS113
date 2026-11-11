"""Hypothesis fuzz tests and regression checks for the Lab 7 self-storage parser.

Run from this directory: python -m pytest -q test_processor.py
Invalid inputs are represented by None; valid inputs preserve the original result.
"""

import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import duration_average, parse_rental, payable_rent


FUZZ_TEXT = st.one_of(st.text(max_size=120), st.none())


@settings(max_examples=200, deadline=None, derandomize=True)
@given(FUZZ_TEXT)
def test_parse_rental_no_crash(text):
    result = parse_rental(text)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], str)
        and bool(result[0])
        and isinstance(result[1], float)
        and math.isfinite(result[1])
        and result[1] >= 0
    )


@settings(max_examples=200, deadline=None, derandomize=True)
@given(FUZZ_TEXT)
def test_duration_average_no_crash(text):
    result = duration_average(text)
    assert result is None or (
        type(result) is int and result >= 0
    )


@settings(max_examples=200, deadline=None, derandomize=True)
@given(FUZZ_TEXT)
def test_payable_rent_no_crash(text):
    result = payable_rent(text)
    assert result is None or (
        isinstance(result, (int, float))
        and math.isfinite(result)
        and result >= 0
    )


@settings(max_examples=100, deadline=None)
@given(
    st.sampled_from(["small", "medium", "large"]),
    st.integers(min_value=0, max_value=100000),
)
def test_parse_rental_valid_values(unit, months):
    assert parse_rental(f" {unit} : {months} ") == (unit.title(), float(months))


@settings(max_examples=100, deadline=None)
@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=1, max_size=50))
def test_duration_average_matches_integer_mean(values):
    assert duration_average(",".join(map(str, values))) == sum(values) // len(values)


@settings(max_examples=100, deadline=None)
@given(
    st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
)
def test_payable_rent_matches_original_formula(rent, discount):
    result = payable_rent(f"{rent}|{discount}")
    expected = max(rent * 1.18 - discount, 0.0)
    assert result == pytest.approx(expected, rel=1e-10, abs=1e-6)


@pytest.mark.parametrize("text", [None, "", "medium", ":5", "medium:", "medium:abc", "medium:-2", "medium:NaN", "medium:inf", "medium:2:extra"])
def test_parse_rental_invalid_values(text):
    assert parse_rental(text) is None


@pytest.mark.parametrize("text", [None, "", ",", "3,,6", "3,", "x,y", "-1,2", "3,2.5", "3|6"])
def test_duration_average_invalid_values(text):
    assert duration_average(text) is None


@pytest.mark.parametrize("text", [None, "", "2400", "|200", "200|", "abc|2", "-1|5", "100|-1", "nan|2", "inf|0", "1.7e308|0", "2400|200|1"])
def test_payable_rent_invalid_values(text):
    assert payable_rent(text) is None


def test_known_good_examples():
    assert parse_rental("medium:6") == ("Medium", 6.0)
    assert duration_average("3,6,12") == 7
    assert payable_rent("2400|200") == pytest.approx(2632.0)
    assert payable_rent("100|200") == pytest.approx(0.0)
