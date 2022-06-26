# from auto_docstring import (
#     find_functions_in_ast,
#     get_return_type_hint,
#     parse_python_code,
#     stringify_type_expression,
# )

# code = "def f() -> Union[str,int]:\n    pass"
# tree = parse_python_code(code)
# functions = find_functions_in_ast(tree)
# type_hint = get_return_type_hint(functions[0])
# stringify_type_expression(type_hint)
