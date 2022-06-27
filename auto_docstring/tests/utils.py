import ast


def get_nth_letter(n: int) -> str:
    return chr(ord("a") + n)


def get_first_statement_as_expr(test_code: str) -> ast.expr:
    tree = ast.parse(test_code)
    first_expression = tree.body[0]
    return first_expression.value  # type: ignore
