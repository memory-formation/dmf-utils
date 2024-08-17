

def copy_docstring(from_func):
    """
    Decorator to copy the docstring from one function to another.

    Parameters
    ----------
    from_func : function
        The function from which the docstring should be copied.

    Returns
    -------
    function
        The decorated function with the copied docstring.
    """
    def decorator(to_func):
        to_func.__doc__ = from_func.__doc__
        return to_func
    return decorator