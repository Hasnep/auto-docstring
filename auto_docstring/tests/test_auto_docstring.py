import ast
from typing import List

import pytest

from auto_docstring import (
    DocstringFunctionArgument,
    FunctionArgument,
    FunctionDef,
    FunctionParts,
    find_functions_in_ast,
    generate_docstring,
    generate_docstring_argument,
    get_return_type_hint,
    indent,
    parse_args_from_docstring,
    parse_python_code,
    stringify_type_expression,
)
from auto_docstring.tests.utils import get_first_statement_as_expr, get_nth_letter

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


@pytest.mark.parametrize(
    ",".join(["python_code", "expected_n_functions"]),
    [
        ("\n\n".join([f"def {get_nth_letter(i)}():\n    pass" for j in range(i)]), i)
        for i in range(10)
    ],
)
def test_find_functions_in_ast(python_code: str, expected_n_functions: int):
    tree = parse_python_code(python_code)
    output = find_functions_in_ast(tree)
    assert len(output) == expected_n_functions


stringify_type_expression_codes = [
    "List[Dict[str, Any]]",
    "Optional[Union[int, MyOtherType]]",
]
stringify_type_expression_input = [
    get_first_statement_as_expr(test_code)
    for test_code in stringify_type_expression_codes
]


@pytest.mark.parametrize(
    ",".join(["type_expression", "expected_output"]),
    zip(stringify_type_expression_input, stringify_type_expression_codes),
)
def test_stringify_type_expression(type_expression: ast.expr, expected_output: str):
    assert stringify_type_expression(type_expression) == expected_output


stringify_type_expression_errors_input = ["alskdj"]


@pytest.mark.parametrize("type_expression", stringify_type_expression_errors_input)
def test_stringify_type_expression_errors(type_expression: ast.expr):
    with pytest.raises(ValueError):
        stringify_type_expression(type_expression)


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


@pytest.mark.skip()
@pytest.mark.parametrize(
    ",".join(["docstring_args", "expected_args"]),
    zip(parse_args_from_docstring_input, parse_args_from_docstring_output),
)
def test_parse_args_from_docstring(
    docstring_args: str, expected_args: List[DocstringFunctionArgument]
):
    output = parse_args_from_docstring(docstring_args)
    assert len(output) == len(expected_args)
    for output_arg, expected_arg in zip(output, expected_args):
        assert output_arg.name == expected_arg.name
        assert output_arg.type_hint == expected_arg.type_hint
        assert output_arg.description == expected_arg.description


@pytest.mark.parametrize(
    ",".join(["test_string", "indent_level", "expected_output"]),
    [
        ("test", 0, "test"),
        ("test", 1, "    test"),
        ("test", 2, "        test"),
        ("test\nstring", 1, "    test\n    string"),
    ],
)
def test_indent(test_string: str, indent_level: int, expected_output: str):
    assert indent(test_string, indent_level) == expected_output


@pytest.mark.skip()
@pytest.mark.parametrize(
    ",".join(["arg", "expected_argument_docstring"]),
    [(FunctionArgument("x", "int"), "x (int): _argument_description_")],
)
def test_generate_docstring_argument(
    arg: FunctionArgument, expected_argument_docstring: str
):
    assert generate_docstring_argument(arg) == expected_argument_docstring


@pytest.mark.skip()
@pytest.mark.parametrize(
    ",".join(["function_parts", "expected_docstring"]),
    [
        (
            FunctionParts(
                "f",
                None,
                [FunctionArgument("x", "int"), FunctionArgument("y", "str")],
                "Optional[int]",
            ),
            """
_function_summary_

Args:
    x (int): _argument_description_
    y (str): _argument_description_

Return:
    Optional[int]: _return_description_
""",
        )
    ],
)
def test_generate_docstring(function_parts: FunctionParts, expected_docstring: str):
    assert generate_docstring(function_parts) == expected_docstring


get_return_type_hint_input = [
    "def f() -> int: pass",
    "def g() -> Optional[Union[str, int]]: pass",
    "def g(): pass",
]
get_return_type_hint_output = ["int", "Optional[Union[str, int]]", None]


@pytest.mark.parametrize(
    ",".join(["function_def", "expected_return_type_hint"]),
    zip(
        [
            find_functions_in_ast(parse_python_code(x))[0]
            for x in get_return_type_hint_input
        ],
        get_return_type_hint_output,
    ),
)
def test_get_return_type_hint(
    function_def: FunctionDef, expected_return_type_hint: str
):
    assert get_return_type_hint(function_def) == expected_return_type_hint
