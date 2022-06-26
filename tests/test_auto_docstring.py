import ast
from typing import List

import pytest

from auto_docstring import (  # extract_docstring_parts,; extract_parts_of_function_def,
    DocstringFunctionArgument,
    find_functions_in_ast,
    parse_args_from_docstring,
    parse_python_code,
    stringify_type_expression,
)

test_code = '''
def f(x: int, y: Optional[Union[str, int]]) -> List[Dict[str, Any]]:
    """
    This is the summary line.

    This is the first line of the description.
    And this is the second line.

    Args:
        x (int): This is the description of the first argument.
            It extends to another line.
        y (Optional[Union[str,int]]): This is the description of the second argument.
            This is the second line of the second argument's description.
    
    Returns:
        List[Dict[str,Any]]: This is the description of the return type.
    """
    pass


def g(x: int, y: Optional[Union[int, MyOtherType]]) -> Optional[Union[int, MyOtherType]]:
    """
    This is the summary line of a function.

    Args:
        x (int): This is the first argument's description.
        y (Optional[Union[int, MyOtherType]]): This is the second argument's description.

    Returns:
        Optional[Union[int, MyOtherType]]: This is the return value's description.
    """
    pass
'''


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


stringify_type_expression_input = [
    f.returns for f in find_functions_in_ast(parse_python_code(test_code))
]
stringify_type_expression_expected_output = [
    "List[Dict[str, Any]]",
    "Optional[Union[int, MyOtherType]]",
]


@pytest.mark.parametrize(
    ",".join(["type_expression", "expected_output"]),
    zip(stringify_type_expression_input, stringify_type_expression_expected_output),
)
def test_stringify_type_expression(type_expression: ast.expr, expected_output: str):
    assert stringify_type_expression(type_expression) == expected_output


parse_args_from_docstring_input = [
    """
        x (int): This is the description of the first argument.
            It extends to another line.
        y (Optional[Union[str,int]]): This is the description of the second argument.
            This is the second line of the second argument's description.
""",
    """
        x (int): This is the first argument's description.
        y (Optional[Union[int, MyOtherType]]): This is the second argument's description.
""",
]
parse_args_from_docstring_output = [
    [
        DocstringFunctionArgument(
            "x",
            "int",
            "This is the description of the first argument.\nIt extends to another line.",
        ),
        DocstringFunctionArgument(
            "y",
            "Optional[Union[str, int]]",
            "This is the description of the second argument.\nThis is the second line of the second argument's description.",
        ),
    ],
    [
        DocstringFunctionArgument(
            "x", "int", "This is the first argument's description."
        ),
        DocstringFunctionArgument(
            "y",
            "Optional[Union[int, MyOtherType]])",
            "This is the second argument's description.",
        ),
    ],
]


@pytest.mark.parametrize(
    ",".join(["docstring_args", "expected_args"]),
    zip(parse_args_from_docstring_input, parse_args_from_docstring_output),
)
def test_parse_args_from_docstring(
    docstring_args: str, expected_args: List[DocstringFunctionArgument]
):
    output = parse_args_from_docstring(docstring_args)
    for output_arg, expected_arg in zip(output, expected_args):
        assert output_arg.name == expected_arg.name
        assert output_arg.type_hint == expected_arg.type_hint
        assert output_arg.description == expected_arg.description
