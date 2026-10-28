# Lab 5 — Static Code Analysis: Parking Lot System

**Name:** Bharat V Bhat  
**SRN:** PES1UG24CS113  
**Section:** B  
**Assigned source:** https://github.com/SETAPESU26/L5_51_parking_lot_system

## Work completed

Analyzed the assigned original `parking_lot_system.py` with Pylint, Bandit, and Flake8, documented and fixed more than four issues, and reran the three analyzers. Security fixes include removing unsafe `eval()` and shell execution, replacing MD5 with SHA-256, and generating PINs using `secrets`.

| Tool | Before | After |
|---|---|---|
| Pylint | 4.10/10 | **10.00/10** |
| Bandit | 5 findings (2 high, 1 medium, 2 low) | **0 findings** |
| Flake8 | 10 violations | **0 violations** |

The six genuine tool-generated outputs are saved under `reports/before/` and `reports/after/`. An empty Flake8 AFTER report indicates no violations. The BEFORE Bandit report has a PowerShell diagnostic preamble, but the security findings and summary are present.

## Deliverables

- `parking_lot_system.py`: corrected Python program
- `issues.md`: identified issue table, original line numbers and fixes
- `reflection.md`: four suggested reflection answers
- `reports/before/`: Pylint, Bandit and Flake8 reports on original code
- `reports/after/`: Pylint, Bandit and Flake8 reports on corrected code

The required three independent fix commits are `59a03c7` (Bandit), `1d7ca66` (Pylint) and `a33b657` (Flake8). A baseline and documentation commits are also retained.

## Execution

From this folder, with Python and the analysis tools installed:

```powershell
python parking_lot_system.py
python -m pylint parking_lot_system.py
python -m bandit parking_lot_system.py
python -m flake8 parking_lot_system.py
```

The corrected demonstration ran successfully, printing a surge fee of 45.0, one vacant slot, and total collections of 60.0, along with other program output. `parking_manifest.txt` is generated at runtime and is not a submission requirement.

**Reflection note:** The supplied three-page handout asks for reflection answers but does not actually print the questions. The four questions in `reflection.md` are explicitly suggested questions; confirm any separately issued official wording with the instructor.
