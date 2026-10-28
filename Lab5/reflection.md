# Lab 5 - Reflection

**Name:** Bharat V Bhat  
**SRN:** PES1UG24CS113  
**Section:** B

**Important:** The supplied three-page handout asks for answers to reflection questions, and the repository mentions **four** questions, but neither source contains their actual wording. The following are four **suggested lab-aligned questions and original responses**, not a claim to reproduce official questions verbatim.

### 1. What kinds of problems can static analysis uncover?

Static code analysis looks for possible bugs, insecure operations and poor style without needing to execute the program. In the given parking-lot code, manual inspection exposed a mutable default list, a bare `except`, unvalidated hours, weak cryptographic choices, unsafe `eval`, and a shell command built from a filename. These defects matter differently: `eval` introduces a serious attack surface, while long lines and inconsistent naming make maintenance more difficult. The committed before/after reports confirm that Bandit reported five findings, Pylint improved from 4.10/10 to 10.00/10, and Flake8 went from ten violations to zero.

### 2. What is the difference between Pylint, Bandit and Flake8?

Pylint gives broader feedback about code quality, structure, names, possible mistakes and a numerical quality score. Bandit focuses on Python security-sensitive patterns such as code execution, weak cryptography and insecure subprocess use. Flake8 checks syntax-adjacent quality and PEP 8 style concerns, such as unused imports, long lines and bare exceptions. The tools complement each other; they do not guarantee that the program is correct or secure.

### 3. How did the fixes improve the parking-lot program?

The price calculation now accepts a numeric multiplier rather than evaluating an arbitrary string. Manifest export no longer invokes a shell, and PINs come from the `secrets` module. A `ParkingLot` object now owns the slots and total collections, preventing different test instances from sharing global state. Slot release checks for unknown IDs explicitly, and booking rejects invalid durations. The manifest is now valid JSON; the demonstration was executed successfully and confirmed parking, fees, availability, manifest export and collection output. Automated regression-test evidence is not included in this submission. These changes improve reliability and explainability while keeping the example straightforward.

### 4. What are the limitations of static analysis, and how should findings be verified?

A tool warning is evidence to investigate, not automatic proof of a runtime problem. Conversely, tools may miss domain-specific mistakes such as negative booking durations, incorrect billing rules, privacy leaks from storing raw licence plates or problems requiring runtime data. I would compare before/after outputs, review findings by severity and reproduce relevant failures with tests. The final submission includes actual tool-generated before/after reports. The verified results are Pylint 10.00/10, zero Bandit findings, and an empty Flake8 report (no violations). Static analysis does not prove complete correctness or security.
