from typing import Callable, List, Union

def register(dictionary: dict, keys: Union[str, List[str]]):
    """
    Decorator to register a function in a dictionary.
    Used to register functions in different modules.

    Parameters
    ----------
    dictionary : dict
        The dictionary where the function will be registered.
    keys : List[str]
        The list of keys that the function
    """
    if isinstance(keys, str):
        keys = [keys]
        
    def decorator(func: Callable):
        for key in keys:
            dictionary[key] = func
        return func

    return decorator