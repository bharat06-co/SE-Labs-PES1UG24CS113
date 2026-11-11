# Lab 7 - Fuzz Testing for Input Validation Bugs

**Bharat V Bhat | PES1UG24CS113 | Section B**

Assigned repository: https://github.com/SETAPESU26/L6_L7_51_self_storage  
Individual repository: https://github.com/bharat06-co/SE-Labs-PES1UG24CS113

## Application

The self-storage Lab 7 starter is preserved in `baseline/processor.py`. The corrected version is in `processor.py`, with Hypothesis tests in `test_processor.py`. These names follow the submission notice. `self_storage.py` retains compatibility with the original assigned module name. Lab 6 is unchanged.

The program contains three functions:

- `parse_rental`: splits a `unit:months` input, validates it, and returns the unit and duration.
- `duration_average`: calculates the floored average of nonnegative integer month values provided as CSV.
- `payable_rent`: calculates the nonnegative payable amount from `rent|discount` with 18% tax.

Invalid input returns `None` rather than causing the program to crash. Normal input results are preserved.

## Testing

The Hypothesis tests in `test_processor.py` exercise the three functions using text, None, valid numeric values, and specific malformed inputs. The independent `test_validation_regression.py` checks the same input-validation rules and 900 seeded valid inputs.

In local regression testing, the original program failed 35 cases and passed 2; the corrected program passed all 37 cases. Execution records are included under `evidence/`.

### Run everything and regenerate the PDF on Windows

From this `Lab7` folder in Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_lab7_windows.ps1
```

The script installs the Python dependencies, executes the original source and the Hypothesis tests, restores the corrected source, verifies the final Hypothesis results, and rebuilds `Lab7_Fuzz_Testing_Report.pdf` using the recorded test output.

The report includes the execution evidence, the test results and complete source code for `processor.py` and `test_processor.py`.

### Individual commands

```powershell
py -m pip install -r requirements.txt
py processor.py
py -m pytest -q test_processor.py
py -m pytest -q test_validation_regression.py
```
