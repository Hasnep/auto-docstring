import ast
import re
from ast import AST, FunctionDef
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class FunctionArgument:
    name: str
    type_hint: Optional[str]


@dataclass
class FunctionParts:
    docstring: Optional[str]
    arguments: List[FunctionArgument]
    return_type_hint: Optional[str]


def parse_python_code(code: str) -> AST:
    return ast.parse(code, type_comments=True)


def find_functions_in_ast(tree: AST) -> List[FunctionDef]:
    # Currently only finds top level functions
    return [node for node in ast.walk(tree) if isinstance(node, FunctionDef)]


def stringify_type_expression(type_expression: ast.expr) -> str:
    if isinstance(type_expression, ast.Name):
        return type_expression.id
    elif isinstance(type_expression, ast.Subscript):
        subscript_name: str = type_expression.value.id  # type: ignore
        return (
            subscript_name
            + "["
            + stringify_type_expression(type_expression.slice)
            + "]"
        )
    elif isinstance(type_expression, ast.Tuple):
        tuple_arguments = [stringify_type_expression(e) for e in type_expression.elts]
        return ", ".join(tuple_arguments)
    else:
        raise ValueError(f"did not recognise type {type(type_expression)}.")


def get_return_type_hint(function_def: FunctionDef) -> Optional[str]:
    return (
        None
        if function_def.returns is None
        else stringify_type_expression(function_def.returns)
    )


def get_function_arguments(function_def: FunctionDef) -> List[FunctionArgument]:
    return [
        FunctionArgument(
            name=a.arg,
            type_hint=None
            if a.annotation is None
            else stringify_type_expression(a.annotation),
        )
        for a in function_def.args.args
    ]


def extract_parts_of_function_def(function_def: FunctionDef) -> FunctionParts:
    arguments = get_function_arguments(function_def)
    return_type = get_return_type_hint(function_def)
    return FunctionParts(
        docstring=ast.get_docstring(function_def),
        arguments=arguments,
        return_type_hint=return_type,
        # function_def.col_offset      ,
        # function_def.end_col_offset  ,
        # function_def.lineno          ,
        # function_def.body            ,
        # function_def.decorator_list  ,
        # function_def.end_lineno      ,
        # function_def.name            ,
        # function_def.type_comment    ,
    )


def split_first(x: str, until_this: str) -> Tuple[str, str, str]:
    index_of_split = x.index(until_this)
    return x[index_of_split:], until_this, x[:index_of_split]


@dataclass
class DocstringParts:
    summary: str
    description: str
    args: str
    raises: str
    returns: str
    yields: str


def extract_docstring_parts(docstring: str) -> DocstringParts:
    pattern = re.compile(
        "".join(
            [
                r"^",  # Start of string
                r"(?: {0,4})?",  # Optional indentation
                r"(?P<summary>.+)",  # One line summary
                r"(?:\n\n(?P<description>(.|\n)+?))?",  # Optional multi-line description
                r"(?:\n\nArgs:\n(?P<args>(.|\n)+?))?",  # Optional list of arguments
                r"(?:\n\nRaises:\n(?P<raises>(.|\n)+))?",  # Optional list of errors raised
                r"(?:\n\nReturns:\n(?P<returns>(.|\n)+?))?",  # Optional list of return values
                r"(?:\n\nYields:\n(?P<yields>(.|\n)+))?",  # Optional list of yield values
                r"\n*",  # Trailing newlines
                "$",  # End of string
            ]
        )
    )
    matches = pattern.match(docstring)
    if matches is None:
        raise ValueError("no matches")
    else:
        return DocstringParts(
            summary=matches.group("summary"),
            description=matches.group("description"),
            args=matches.group("args"),
            raises=matches.group("raises"),
            returns=matches.group("returns"),
            yields=matches.group("yields"),
        )


@dataclass
class DocstringFunctionArgument:
    name: str
    type_hint: Optional[str]
    description: str


def parse_args_from_docstring(docstring_args: str) -> List[DocstringFunctionArgument]:
    docstring_args = docstring_args.strip()
    args: List[DocstringFunctionArgument] = []
    argument_pattern = re.compile(
        r"^(?P<name>\w+) \((?P<type_hint>.+)\): (?P<description>.+)$"
    )
    found_an_arg = False
    name: str = ""
    type_hint: str = ""
    description: str = ""
    for line in docstring_args.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue
        matches = argument_pattern.match(line)
        if matches:
            if found_an_arg:
                argument = DocstringFunctionArgument(
                    name=name, type_hint=type_hint, description=description
                )
                args.append(argument)

            name = matches.group("name")
            type_hint = matches.group("type_hint")
            description = matches.group("description")
            found_an_arg = True
        else:
            if found_an_arg:
                description += "\n" + line
            else:
                raise ValueError(
                    "Found an argument description without defining an argument."
                )
    return args

def generate_docstring_argument(arg:FunctionArgument)->str:
    

def generate_docstring(function:FunctionParts)->str:
    function.arguments
