"""Input-safe storage rental parser, duration average, and payable rent calculator.

Return None for malformed/invalid inputs rather than raising exceptions.
Valid inputs preserve the starter application's results.
"""

import math


def parse_rental(text):
    """Return (title-cased unit, nonnegative months) or None for invalid input."""
    if not isinstance(text, str) or text.count(":") != 1:
        return None
    unit, months_text = text.split(":")
    unit = unit.strip()
    if not unit or not months_text.strip():
        return None
    try:
        months = float(months_text)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(months) or months < 0:
        return None
    return unit.title(), months


def duration_average(months_csv):
    """Return floor of average nonnegative whole-month durations; else None."""
    if not isinstance(months_csv, str) or not months_csv.strip():
        return None
    parts = months_csv.split(",")
    if any(not p.strip() for p in parts):
        return None
    try:
        values = [int(p.strip()) for p in parts]
    except (ValueError, OverflowError):
        return None
    if any(v < 0 for v in values):
        return None
    return sum(values) // len(values)


def payable_rent(text):
    """Return nonnegative rent with 18% tax and discount; else None."""
    if not isinstance(text, str) or text.count("|") != 1:
        return None
    rent_text, discount_text = text.split("|")
    if not rent_text.strip() or not discount_text.strip():
        return None
    try:
        rent = float(rent_text)
        discount = float(discount_text)
    except (ValueError, OverflowError):
        return None
    if not all(math.isfinite(x) and x >= 0 for x in (rent, discount)):
        return None
    total = rent * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0.0)


def main():
    print("==== Running parse_rental ====")
    user_input = input("Enter unit:months (e.g. medium:6): ")
    result = parse_rental(user_input)
    print("Unit and Months:", result if result is not None else "Invalid rental details")

    print("\n==== Running duration_average ====")
    user_input = input("Enter rental months as CSV (e.g. 3,6,12): ")
    result = duration_average(user_input)
    print("Average Duration:", result if result is not None else "Invalid rental durations")

    print("\n==== Running payable_rent ====")
    user_input = input("Enter rent|discount (e.g. 2400|200): ")
    result = payable_rent(user_input)
    print("Payable Rent:", result if result is not None else "Invalid rent or discount")


if __name__ == "__main__":
    main()
