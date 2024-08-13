from typing import Callable, Optional
from datetime import datetime

from .alerts import send_alert

__all__ = ["alert"]

def _to_str(object, max_length: int = 100) -> str:
    text = str(object)
    if max_length and len(text) > max_length:
        text = text[:max_length - 3] + "..."
    return text

def alert(func: Optional[Callable] = None, *, output: bool = False, max_length: int = 100) -> Callable:
    """
    Decorator that sends an alert after the execution of the decorated function.
    
    Can be used with or without parentheses:
    - @alert
    - @alert(output=True)

    :param func: The function to be decorated.
    :param output: If True, include the function's output in the alert message.
    :return: The decorator function.
    """
    if func is None:
        # Used as @alert(output=True) with parentheses
        def decorator(inner_func: Callable) -> Callable:
            return _alert_decorator(inner_func, output=output, max_length=max_length)
        return decorator
    else:
        # Used as @alert without parentheses
        return _alert_decorator(func, output=output)

def _alert_decorator(func: Callable, output: bool, max_length: int = 100) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        params = {
            ":calendar: Start Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            message = f"Execution of function *{func.__name__}* finished successfully.\n"
            params[":bell: End Time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
            params[":stopwatch: Duration"] = str(end_time - start_time).split(".")[0]

            if output:
                params[":outbox_tray: Output"] = f"_{_to_str(result)}_"

            send_alert(text=message, level="success", params=params)
            return result
        except Exception as e:
            end_time = datetime.now()
            message = f"Execution of function *{func.__name__}* failed with an error.\n"
            params[":bell: End Time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
            params[":stopwatch: Duration"] = str(end_time - start_time).split(".")[0]
            params[f":exclamation: {e.__class__.__name__}"] = f"_'{str(e)}'_"

            send_alert(text=message, level="error", params=params)
            raise e

    return wrapper
