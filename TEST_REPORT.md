# Test Report

Generated at: 2026-03-28 09:24:42 CST

## Scope

- Project: `sqb-payment-reference-py-app`
- Test command: `PYTHONPATH=. .venv/bin/pytest -v --junitxml=test-report.xml`
- XML report: `test-report.xml`

## Environment

- OS: macOS (darwin)
- Python used: `3.9.6`
- Project requirement from `pyproject.toml`: `>=3.11`

## Summary

- Total collected test modules: 5
- Passed: 0
- Failed: 0
- Errors: 5
- Skipped: 0
- Total runtime: 0.468s

## Result

The test suite did not reach test execution. It failed during collection because the current runtime is Python 3.9, while the project code uses Python 3.10+/3.11+ features.

## Error Breakdown

1. `tests/test_health.py`
   - Collection error in `app/support/signing.py`
   - Error: `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`
   - Cause: `str | None` union syntax is not supported at runtime in Python 3.9 without postponed evaluation.

2. `tests/test_payment_endpoints.py`
   - Collection error in `app/support/signing.py`
   - Error: `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`

3. `tests/test_signing.py`
   - Collection error in `app/support/signing.py`
   - Error: `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`

4. `tests/test_status_parser.py`
   - Import error in `app/protocol/status.py`
   - Error: `ImportError: cannot import name 'StrEnum' from 'enum'`
   - Cause: `enum.StrEnum` is available in Python 3.11+, not Python 3.9.

5. `tests/test_terminal_and_notify.py`
   - Collection error in `app/support/signing.py`
   - Error: `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`

## Conclusion

This run confirms an environment mismatch, not necessarily a functional defect in the application logic.

To obtain a valid project-level test result, rerun the suite in a Python 3.11+ environment and install dependencies from `pyproject.toml`.
