from auto_docstring import (
    check_docstring,
    extract_parts_of_function_def,
    find_functions_in_ast,
    parse_python_code,
)
from auto_docstring.cli import get_cli_arguments

file_paths = get_cli_arguments()
for file_path in file_paths:
    print(file_path)
    with open(file_path, "r") as f:
        test_code = f.read()
    the_ast = parse_python_code(test_code)
    functions = find_functions_in_ast(the_ast)
    functions = [extract_parts_of_function_def(f) for f in functions]
    for function in functions:
        print(function.name)
        docstring_errors = check_docstring(file_path, function)
        if len(docstring_errors) > 0:
            for docstring_error in docstring_errors:
                print(docstring_error.get_message())
        else:
            print(f"Function `{function.name}` is good!")
