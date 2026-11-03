# Lab 6 - Code and Branch Coverage Analysis

**Student:** Bharat V Bhat | **SRN:** PES1UG24CS113 | **Section:** B

- Assigned starter repository: https://github.com/SETAPESU26/L6_L7_51_self_storage
- Individual lab repository: https://github.com/bharat06-co/SE-Labs-PES1UG24CS113

## Purpose

Measure line and branch coverage of the unmodified `self_storage.py` module using pytest and coverage.py. The required minimum is 90% for each.

## Test cases

- `CodeCoverageTest_self_storage_application.py`: 11 tests, 100% line coverage (37 of 37 statements).
- `BranchCoverageTest_self_storage_application.py`: 30 parameterized tests, 100% branch coverage (26 of 26 branches, 0 partial).
- `test_self_storage.py`: original starter tests provided in the assignment.

## Commands

From this `Lab6` folder:

```powershell
py -m pip install pytest coverage
py -m coverage run --source=self_storage -m pytest -q CodeCoverageTest_self_storage_application.py
py -m coverage report -m
py -m coverage run --branch --source=self_storage -m pytest -q BranchCoverageTest_self_storage_application.py
py -m coverage report -m
```

Terminal screenshot evidence and text outputs from real local Linux test executions are in `evidence/`. The original application file is not modified.

## Version-control requirement

Lab 6 is committed in two separate commits: one for code coverage and a second for branch coverage.
