def f(x: int, y: Optional[Union[str, int]]) -> List[Dict[str, Any]]:
    """
    This is the summary line.

    This is the first line of the description.
    And this is the second line.

    Args:
        x (int): This is the description of the first argument.
            It extends to another line.
        y (Optional[Union[str,int]]): This is the description of the second argument.
            This is the second line of the second argument's description.
    
    Returns:
        List[Dict[str,Any]]: This is the description of the return type.
    """
    pass


def g(x: int, y: Optional[Union[int, MyOtherType]]) -> Optional[Union[int, MyOtherType]]:
    """
    This is the summary line of a function.

    Args:
        x (int): This is the first argument's description.
        y (Optional[Union[int, MyOtherType]]): This is the second argument's description.

    Returns:
        Optional[Union[int, MyOtherType]]: This is the return value's description.
    """
    pass
