from pathlib import Path


class DocstringError:
    def __init__(self, file_path: Path, function_name: str):
        self.function_name = function_name
        self.file_path = file_path
        # line_number: int  # TODO: implement


class IncorrectArgumentTypehintError(DocstringError):
    def __init__(self, file_path: Path, function_name: str, argument_name: str):
        super().__init__(file_path, function_name)
        self.argument_name = argument_name

    def get_message(self) -> str:
        return f"Function `{self.function_name}` argument `{self.argument_name}` has the wrong type hint."


class IncorrectReturnTypehintError(DocstringError):
    def __init__(self, file_path: Path, function_name: str):
        super().__init__(file_path, function_name)

    def get_message(self) -> str:
        return ""


class MissingArgsSectionError(DocstringError):
    def __init__(self, file_path: Path, function_name: str):
        super().__init__(file_path, function_name)

    def get_message(self) -> str:
        return ""


class MissingArgumentTypehintError(DocstringError):
    def __init__(self, file_path: Path, function_name: str, argument_name: str):
        super().__init__(file_path, function_name)
        self.argument_name = argument_name

    def get_message(self) -> str:
        return f"Function `{self.function_name}` argument `{self.argument_name}` did not have a type hint."


class MissingArgumentError(DocstringError):
    def __init__(self, file_path: Path, function_name: str, argument_name: str):
        super().__init__(file_path, function_name)
        self.argument_name = argument_name

    def get_message(self) -> str:
        return f"Function `{self.function_name}` argument `{self.argument_name}` did not have a type hint."


class MissingDocstringError(DocstringError):
    def __init__(self, file_path: Path, function_name: str):
        super().__init__(file_path, function_name)

    def get_message(self) -> str:
        return f"Function `{self.function_name}` is missing a docstring."


class MissingReturnTypehintError(DocstringError):
    def __init__(self, file_path: Path, function_name: str):
        super().__init__(file_path, function_name)

    def get_message(self) -> str:
        return ""


class MissingReturnsSectionError(DocstringError):
    def __init__(self, file_path: Path, function_name: str):
        super().__init__(file_path, function_name)

    def get_message(self) -> str:
        return ""


class MissingSummaryError(DocstringError):
    def __init__(self, file_path: Path, function_name: str):
        super().__init__(file_path, function_name)

    def get_message(self) -> str:
        return ""


class UndocumentedArgumentError(DocstringError):
    def __init__(self, file_path: Path, function_name: str, argument_name: str):
        super().__init__(file_path, function_name)
        self.argument_name = argument_name

    def get_message(self) -> str:
        return ""
