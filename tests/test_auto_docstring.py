import ast
import pytest

from auto_docstring import find_functions_in_ast, parse_python_code,stringify_type_expression


def _get_nth_letter(n: int) -> str:
    return chr(ord("a") + n)


@pytest.mark.parametrize(
    ",".join(["python_code", "expected_n_functions"]),
    [
        ("\n\n".join([f"def {_get_nth_letter(i)}():\n    pass" for j in range(i)]), i)
        for i in range(10)
    ],
)
def test_find_functions_in_ast(python_code: str, expected_n_functions: int):
    tree = parse_python_code(python_code)
    output = find_functions_in_ast(tree)
    assert len(output) == expected_n_functions



@pytest.mark.parameterize(",".join(["type_expression","expected_output"]),[() ])
def test_stringify_type_expression(type_expression:ast.expr,expected_output:str):
    assert stringify_type_expression(type_expression)==expected_output
