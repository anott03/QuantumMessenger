# API
This directory contains all the source code for the API.

### Testing
We use [pytest](https://pytest.org) for testing. Tests are grouped by class. Per pytest specs, all test classes are prefixed with `Test` (ex. `TestBB84`) and all test functions are prefixed with `test_` (ex. `test_random_number`). All tests are contained in the `test` directory.

To run a set of tests, use the following command: `pytest -q {filename}`.
