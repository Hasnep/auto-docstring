from typing import Tuple


def split_first(x: str, until_this: str) -> Tuple[str, str, str]:
    index_of_split = x.index(until_this)
    return x[index_of_split:], until_this, x[:index_of_split]
