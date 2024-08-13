from typing import Callable, Optional
from datetime import datetime
from pathlib import Path

from .alerts import send_alert

__all__ = ["alert"]


def alert(
    func: Optional[Callable] = None,
    *,
    output: bool = False,
    input: bool = False,
    max_length: int = 100,
) -> Callable:
    """
    Decorator that sends an alert after the execution of the decorated function.

    Can be used with or without parentheses:
    - @alert
    - @alert(output=True, input=True)

    :param func: The function to be decorated.
    :param output: If True, include the function's output in the alert message.
    :param input: If True, log the input parameters (args and kwargs).
    :param max_length: Maximum length of the output string to be logged.
    :return: The decorator function.
    """
    if func is None:
        # Used as @alert(output=True, input=True) with parentheses
        def decorator(inner_func: Callable) -> Callable:
            return _alert_decorator(
                inner_func, output=output, input=input, max_length=max_length
            )

        return decorator
    else:
        # Used as @alert without parentheses
        return _alert_decorator(func, output=output, input=input, max_length=max_length)


def _alert_decorator(
    func: Callable,
    output: bool,
    input: bool,
    max_length: int,
    max_attach_size: int = 10 * 1024 * 1024,
) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        attachment = None
        params = {
            ":calendar: Start Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            ":bell: End Time": "",
            ":stopwatch: Duration": "",
        }
        if input:
            input_str = _input_to_str(args, kwargs, input, max_length)
            if input_str:
                params[":inbox_tray: Input"] = input_str

        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            message = f"Execution of function *{func.__name__}* finished successfully."
            params[":bell: End Time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
            params[":stopwatch: Duration"] = str(end_time - start_time).split(".")[0]

            if output:
                params[":outbox_tray: Output"] = f"_{_to_str(result)}_"
                # Check is a file path and not too large
                if (
                    isinstance(result, Path)
                    and result.exists()
                    and result.stat().st_size < max_attach_size
                ):
                    attachment = result

            send_alert(
                text=message, level="success", params=params, attachment=attachment
            )
            return result
        except Exception as e:
            end_time = datetime.now()
            message = f"Execution of function *{func.__name__}* failed with an error."
            params[":bell: End Time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
            params[":stopwatch: Duration"] = str(end_time - start_time).split(".")[0]
            params[f":exclamation: {e.__class__.__name__}"] = f"_'{str(e)}'_"

            send_alert(text=message, level="error", params=params)
            raise e

    return wrapper


def _to_str(object, max_length: int = 100) -> str:
    text = str(object)
    if max_length and len(text) > max_length:
        text = text[: max_length - 3] + "..."
    return text


def _input_to_str(args, kwargs, input, max_length: int = 100) -> str:
    input_str = ""
    sep = "\n" + 10 * " " + "• "
    if input is True:
        for i, arg in enumerate(args, 1):
            input_str += f"{sep}*arg{i}*: _{_to_str(arg, max_length)}_"
    for key, value in kwargs.items():
        if input is True or key in input:
            input_str += f"{sep}*{key}*: _{_to_str(value, max_length)}_"
    return input_str
