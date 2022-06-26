from auto_docstring import (
    check_docstring,
    extract_parts_of_function_def,
    find_functions_in_ast,
    get_cli_arguments,
    parse_python_code,
)

file_paths = get_cli_arguments()
for file_path in file_paths:
    with open(file_path, "r") as f:
        test_code = f.read()
    the_ast = parse_python_code(test_code)
    functions = find_functions_in_ast(the_ast)
    functions = [extract_parts_of_function_def(f) for f in functions]
    for function in functions:
        check_docstring(function)
