"""Line-coverage tests for the supplied self-storage application.

Run: python -m coverage run --source=self_storage -m pytest -q CodeCoverageTest_self_storage_application.py
"""

import pytest

from self_storage import access_allowed, payment_status, rent_due


def test_rejects_unknown_unit_size():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("extra-large", 2, False, False)


def test_rejects_negative_months():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)


def test_member_gets_one_extra_covered_month():
    assert rent_due("small", 2, False, True) == 0


def test_standard_non_climate_rent():
    # Medium deposits cover two months; the next two cost 80 each.
    assert rent_due("medium", 4, False, False) == 160


def test_long_term_climate_rent():
    # One covered month, then nine at the discounted climate rate (120 - 10 - 5).
    assert rent_due("small", 10, True, False) == 945


def test_owner_can_access_outside_regular_hours():
    assert access_allowed(1, 4, True) is True


def test_non_owner_cannot_access_before_opening():
    assert access_allowed(5, 1, False) is False


def test_non_owner_can_access_during_open_hours():
    assert access_allowed(12, 2, False) is True


def test_autopay_account_is_current_at_cutoff():
    assert payment_status(0, True, False) == "current"


def test_previous_late_payment_grace_period():
    # Manual-pay cutoff is 5, increased to 15 for a prior late payment.
    assert payment_status(0, False, True) == "grace"


def test_overdue_account_enters_lien_status():
    assert payment_status(-11, False, False) == "lien"
