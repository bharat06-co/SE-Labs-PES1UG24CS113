"""Branch-coverage tests for the supplied self-storage application.

Run: python -m coverage run --branch --source=self_storage -m pytest -q BranchCoverageTest_self_storage_application.py
"""

import pytest

from self_storage import access_allowed, payment_status, rent_due


@pytest.mark.parametrize(
    ("unit_size", "months", "climate", "member", "expected"),
    [
        ("small", 1, False, False, 0),   # Deposit exactly covers stay
        ("small", 2, False, True, 0),    # Membership increases covered months
        ("large", 3, False, True, 0),    # Large units receive no member extension
        ("large", 4, False, True, 80),   # Large unit: first billable month
        ("medium", 4, False, False, 160),# Standard rate, at most six extra months
        ("small", 2, True, False, 120),  # Climate rate without long-stay discount
        ("small", 8, False, False, 490), # Long stay, non-climate: 7 * (80 - 10)
        ("small", 8, True, False, 735),  # Long stay, climate: 7 * (120 - 10 - 5)
        ("small", 3, False, True, 80),   # Member has one billable month after deposit
    ],
)
def test_rent_due_valid_cases(unit_size, months, climate, member, expected):
    assert rent_due(unit_size, months, climate, member) == expected


@pytest.mark.parametrize(
    ("unit_size", "months", "error"),
    [
        ("unknown", 1, "unknown unit size"),
        ("small", -1, "invalid months"),
    ],
)
def test_rent_due_invalid_cases(unit_size, months, error):
    with pytest.raises(ValueError, match=error):
        rent_due(unit_size, months, False, False)


@pytest.mark.parametrize(
    ("hour", "visitors", "is_owner", "expected"),
    [
        (1, 4, True, True),    # Owners bypass hour restriction, up to four visitors
        (1, 5, True, False),   # Owners are still limited to four visitors
        (5, 1, False, False),  # Non-owners: before opening
        (23, 1, False, False), # Non-owners: after closing
        (6, 2, False, True),   # Opening-time boundary
        (22, 2, False, True),  # Closing-time boundary
        (12, 3, False, False), # Non-owner visitor limit exceeded
    ],
)
def test_access_allowed_cases(hour, visitors, is_owner, expected):
    assert access_allowed(hour, visitors, is_owner) is expected


@pytest.mark.parametrize(
    ("days_to_due", "autopay", "prior_late", "expected"),
    [
        (0, True, False, "current"),     # Autopay cutoff = 0
        (-15, True, False, "grace"),    # Grace lower boundary
        (-16, True, False, "lien"),     # Just outside grace
        (5, False, False, "current"),   # Manual-pay cutoff = 5
        (4, False, False, "grace"),     # Just below current cutoff
        (-11, False, False, "lien"),    # Manual-pay grace has ended
        (10, True, True, "current"),    # Prior late adds ten days to cutoff
        (9, True, True, "grace"),       # Autopay with late history
        (-6, True, True, "lien"),       # Just below late-history grace
        (15, False, True, "current"),  # Manual-pay with late history
        (0, False, True, "grace"),      # Its grace lower boundary
        (-1, False, True, "lien"),      # Just outside that boundary
    ],
)
def test_payment_status_cases(days_to_due, autopay, prior_late, expected):
    assert payment_status(days_to_due, autopay, prior_late) == expected
