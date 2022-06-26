import ast
from typing import List

import pytest

from auto_docstring import (  # extract_docstring_parts,; extract_parts_of_function_def,
    DocstringFunctionArgument,
    FunctionArgument,
    FunctionParts,
    find_functions_in_ast,
    generate_docstring,
    generate_docstring_argument,
    indent,
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


@pytest.mark.parametrize(
    ",".join(["arg", "expected_argument_docstring"]),
    [(FunctionArgument("x", "int"), "x (int): _argument_description_")],
)
def test_generate_docstring_argument(
    arg: FunctionArgument, expected_argument_docstring: str
):
    assert generate_docstring_argument(arg) == expected_argument_docstring


@pytest.mark.parametrize(
    ",".join(["function_parts", "expected_docstring"]),
    [
        (
            FunctionParts(
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
