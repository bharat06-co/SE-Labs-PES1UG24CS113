# Lab 5 - Static Code Analysis: Issue Table

**Name:** Bharat V Bhat  
**SRN:** PES1UG24CS113  
**Section:** B  
**Repository:** https://github.com/SETAPESU26/L5_51_parking_lot_system

These findings were initially identified by manual inspection and then checked against the **actual Pylint, Bandit, and Flake8 BEFORE reports** in `reports/before/`. Line numbers refer to the **original** supplied Python file. The reported Bandit severities are: B324 and B605 **High**, B307 **Medium**, B110 and B311 **Low**. Additional manual findings are explicitly design/logic observations rather than claims that a tool detected them.

| Issue | Type / expected tool | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe `eval()` | Security, high priority (Bandit B307) | 46-49 | A surge expression is evaluated as arbitrary Python code, permitting command execution if untrusted. | Accept only a numeric multiplier and multiply by the base rate. |
| Shell command constructed from filename | Security, high priority (Bandit B605/B607 candidate) | 60-64 | Shell-based `os.system()` can interpret metacharacters in user-provided file names. | Replace shell execution with a normal Python `print()`. |
| MD5 vehicle hash | Security (Bandit B324 candidate) | 52-53 | MD5 has known collision weaknesses and is inappropriate for security-sensitive hashes. | Use `hashlib.sha256()`. Hashing alone does not anonymise licence plates. |
| Predictable ticket PIN | Security (Bandit B311 candidate) | 56-57 | `random.randint()` is not intended for secret or security-sensitive PINs. | Use `secrets.randbelow(9000) + 1000`. |
| Hardcoded barrier secret displayed | Security (Bandit B105 candidate) | 75-85 | A secret-like token is embedded in code and printed to stdout. | Remove the unused token and secret disclosure entirely. |
| Mutable default parameter | Logic/quality (Pylint W0102 candidate) | 15 | The `entry_logs=[]` list is reused across independent calls. | Default to `None` and append only to the caller-provided list. |
| Bare except suppresses errors | Reliability/style (Pylint W0702, Flake8 E722 candidates) | 27-33 | Exceptions are swallowed silently, masking erroneous slot IDs or other bugs. | Check slot existence/state explicitly; return success or failure. |
| Zero/negative booking duration | Logic (manual) | 15-22 | A negative or zero hour value would be accepted and could distort total collection. | Reject non-positive or non-integer durations. |
| Files not safely managed | Reliability (Pylint R1732 candidate) | 60-63 | Manual open/close handling is brittle if writing fails. | Use `Path.write_text(..., encoding="utf-8")` and structured JSON. |
| Unused variable and imports | Quality (Pylint/Flake8 candidates) | 1-4, 36-38 | `math` and `overtime_fee` are never used. | Remove unused code. |
| `== None` comparison | Style (Flake8 E711 candidate) | 38 | PEP 8 recommends identity checks; the condition is unnecessarily verbose. | Use a direct `slot is None` check / simplified Boolean expression. |
| Camel-case function names | Style (Pylint C0103 candidate) | 15, 27, 36, 46, 52, 56, 60, 67 | Python function names do not follow `snake_case` convention. | Rename methods to descriptive `snake_case` names. |
| Long lines | Style (Flake8 E501 candidate) | 7-9, 23, 80 | Several lines exceed conventional PEP 8 limits. | Break long literals and statements into readable blocks. |
| Global mutable accounting state | Design (manual/Pylint) | 12, 16, 22 | Bookings mutate a process-wide variable, reducing test isolation. | Encapsulate slots and collected fees within a `ParkingLot` instance. |
| Script runs on import | Testability (manual) | 88 | Importing the module immediately performs a demo and writes a manifest. | Add `if __name__ == "__main__":` guard. |

## Outcome

The corrected script addresses more than four issues and continues to demonstrate booking, releasing, availability, 1.5x surge fees, PIN generation, and manifest export. It now writes JSON and exposes a numeric `surge_multiplier` argument instead of an expression string. **Verified results:** Pylint **4.10/10 → 10.00/10**; Bandit **5 → 0 findings**; Flake8 **10 → 0 violations**. The tool-generated before/after reports are committed under `reports/` and the corrected demo ran successfully on Python 3.13.0.
