import argparse
from pathlib import Path
from typing import List


def get_cli_arguments() -> List[Path]:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_paths", nargs="*")
    arguments = parser.parse_args()
    return arguments.file_paths
