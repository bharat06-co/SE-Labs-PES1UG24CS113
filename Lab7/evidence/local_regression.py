"""Additional deterministic regression test runner (independent of Hypothesis)."""
import importlib.util
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(module, label):
    cases = {
        "parse_rental": [None, "", "small", ":5", "medium:", "medium:abc", "small:-1", "medium:inf", "medium:2:3"],
        "duration_average": [None, "", ",", "3,,6", "3,", "x,y", "-1,2", "3,2.5"],
        "payable_rent": [None, "", "100", "|200", "200|", "abc|2", "-1|5", "100|-1", "nan|2", "inf|0", "1.7e308|0"],
    }
    crashes = 0
    wrong = 0
    for fname, inputs in cases.items():
        for value in inputs:
            try:
                result = getattr(module, fname)(value)
                if result is not None:
                    wrong += 1
            except Exception:
                crashes += 1
    rng = random.Random(20261111)
    ran = 0
    for _ in range(300):
        unit = rng.choice(["small", "medium", "large"])
        months = rng.randint(0, 5000)
        assert module.parse_rental(f" {unit} : {months}") == (unit.title(), float(months))
        vals = [rng.randint(0, 500) for i in range(rng.randint(1, 30))]
        assert module.duration_average(",".join(map(str, vals))) == sum(vals) // len(vals)
        rent = rng.randint(0, 100000)
        discount = rng.randint(0, 100000)
        assert math.isclose(module.payable_rent(f"{rent}|{discount}"), max(rent * 1.18 - discount, 0), abs_tol=1e-7)
        ran += 3
    print(f"{label} - 28 malformed-input cases: {crashes} crashes; {wrong} invalid-value acceptances")
    print(f"{label} - {ran} generated valid-input checks passed")
    return crashes, wrong


if __name__ == "__main__":
    original = load(ROOT / "baseline" / "processor.py", "baseline_processor")
    corrected = load(ROOT / "processor.py", "corrected_processor")
    baseline = check(original, "Original")
    fixed = check(corrected, "Corrected")
    assert sum(baseline) > 0
    assert fixed == (0, 0)
    print("Independent local regression verification: PASS")
