
# Lab 7 - Fuzz Testing for Input Validation Bugs

**Name:** Bharat V Bhat  
**SRN:** PES1UG24CS113  
**Section:** B

## Objective

Identify and fix input validation bugs in the self-storage application using Hypothesis fuzz testing.

## Application

The application contains three functions:

- `parse_rental()` - Parses unit type and rental duration.
- `duration_average()` - Calculates the average rental duration.
- `payable_rent()` - Calculates payable rent after tax and discount.

## Files

- `processor.py` - Corrected application
- `test_processor.py` - Hypothesis fuzz tests
- `baseline/processor.py` - Original application
- `Lab7_Fuzz_Testing_Report.pdf` - Test execution evidence and source code

## Execution

```powershell
py -m pip install -r requirements.txt
py processor.py
py -m pytest test_processor.py
```

## Test Results

| Application | Passed | Failed |
|-------------|--------|--------|
| Original | 4 | 34 |
| Corrected | 38 | 0 |

All 38 tests passed after correcting the input validation bugs.

## Repository

**Assigned Repository:** https://github.com/SETAPESU26/L6_L7_51_self_storage
