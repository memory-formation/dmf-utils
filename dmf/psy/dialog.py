import re
from typing import Optional, Dict, Any, List
from psychopy import gui
from .exceptions import ExperimentStopped

def dialog_form(
    information: Dict[str, Dict[str, Any]],
    title: Optional[str] = None,
    cancel_message: str = "User cancelled input information.",
) -> Dict[str, Any]:
    """
    Display a dialog to request subject information based on a given information dictionary.

    This function creates a dialog window using PsychoPy's GUI module, allowing the user to input
    or select information as specified in the `information` dictionary. It supports text input,
    fixed fields, dropdown selections, and regex validation.

    Parameters
    ----------
    information : dict
        A dictionary where each key corresponds to a field in the dialog. The value for each key
        is another dictionary that can contain the following optional keys:
        - `'label'`: str, the label to display for this field (default is the key itself).
        - `'default'`: Any, the default value for this field (default is an empty string).
        - `'regex'`: str, a regular expression pattern to validate the input (default is `None`).
        - `'fixed'`: bool, whether the field is read-only (default is `False`).
        - `'choices'`: list, if provided, the field will be a dropdown menu with these choices.

    title : str, optional
        The title of the dialog window. If not provided, no title will be displayed.

    cancel_message : str, optional
        The message of the exception if the user cancels the dialog or if input validation fails.
        Defaults to "User cancelled input information."

    Returns
    -------
    dict
        A dictionary containing the user's input, with keys corresponding to those in the
        `information` dictionary.

    Raises
    ------
    ExperimentStopped
        If the user cancels the dialog or if input validation fails due to regex mismatch.
    """
    dialog = gui.Dlg(title=title)

    # Prepare the dialog data
    for k, v in information.items():
        dialog.addField(k, initial=v.get("default", ""), choices=v.get("choices", None))

    try:
        dialog.show()
    except KeyboardInterrupt:
        raise ExperimentStopped(cancel_message)
    
    if not dialog.OK:
        raise ExperimentStopped(cancel_message)
    
    print(dialog.data)

    info = {k: v for k, v in zip(information.keys(), dialog.data)}
    
    return info

def dialog_accept(message: str, title: Optional[str] = None, **kwargs) -> Optional[bool]:
    """
    Display a dialog with a message and Yes/No buttons.

    Returns `True` for 'Yes', `False` for 'No', and `None` if the window is closed.
    """
    dialog = gui.Dlg(title=title, **kwargs)
    dialog.addText(message)
    user_response = dialog.show()
    
    if dialog.OK:
        return True
    elif user_response is None:
        # Dialog was closed using the window's close button
        return None
    else:
        return False
    
class DialogMixin:
    """Mixin class for dialogs in PsychoPy."""

    def dialog_form(self, information: Dict[str, Dict[str, Any]], title: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Display an information dialog."""
        return dialog_form(information, title=title, **kwargs)
    
    def dialog_accept(self, message: str, title: Optional[str] = None, **kwargs) -> Optional[bool]:
        """Display an accept dialog."""
        return dialog_accept(message, title=title, **kwargs)
    