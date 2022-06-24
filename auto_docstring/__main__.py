from auto_docstring import (
    extract_docstring_parts,
    extract_parts_of_function_def,
    find_functions_in_ast,
    parse_python_code,
)

test_code = '''
def f(x: int,y:Optional[Union[int,MyOtherType]]) -> Optional[Union[int,MyOtherType]]:
    """Add one to the number"""
    return x + 1

f(10)
'''

the_ast = parse_python_code(test_code)
functions = find_functions_in_ast(the_ast)
f = functions[0]
args = f.args.args
arg = args[1]
ann = arg.annotation

functions = [extract_parts_of_function_def(f) for f in functions]
print(functions)


for function in functions:
    if function.docstring is not None:
        docstring_parts = extract_docstring_parts(function.docstring)
        print(docstring_parts)
