from auto_docstring import (
    extract_docstring_parts,
    extract_parts_of_function_def,
    find_functions_in_ast,
    parse_args_from_docstring,
    parse_python_code,
)

test_code = ""
the_ast = parse_python_code(test_code)
functions = find_functions_in_ast(the_ast)
functions = [extract_parts_of_function_def(f) for f in functions]
print(functions)


for function in functions:
    if function.docstring is not None:
        docstring_parts = extract_docstring_parts(function.docstring)
        docstring_args = parse_args_from_docstring(docstring_parts.args)
        print(function.arguments)
        print(docstring_args)
