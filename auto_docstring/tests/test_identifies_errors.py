from pathlib import Path

import pytest

from auto_docstring import (
    check_docstring,
    extract_parts_of_function_def,
    find_functions_in_ast,
    parse_python_code,
)

test_cases_folder = Path(".") / "auto_docstring" / "tests" / "test_cases"
test_cases_file_paths = list(test_cases_folder.glob("*.py"))
test_cases = zip(
    [str(p) for p in test_cases_file_paths],
    [p.read_text() for p in test_cases_file_paths],
)


@pytest.mark.skip()
@pytest.mark.parametrize(",".join(["test_case_name", "test_case_code"]), test_cases)
def test_bad_code_fails_check(test_case_name: str, test_case_code: str):
    first_function_definition = find_functions_in_ast(
        parse_python_code(test_case_code)
    )[0]
    first_function_definition_parts = extract_parts_of_function_def(
        first_function_definition
    )
    assert check_docstring(first_function_definition_parts) is False
