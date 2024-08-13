from typing import Optional, TYPE_CHECKING, Union, Literal
import os

if TYPE_CHECKING:
    from .backend import AlertBackend
    from datetime import datetime, timedelta
    from pathlib import Path

ALERT_TOKEN = "DMF_ALERTS_TOKEN" # Environment variable for the alert token

backend = None # Global variable to store the backend instance

__all__ = ["alert", "send_alert", "send_message", "get_backend"]

def send_message(
    text: str = "",
    attachment: Optional[Union[str, "Path"]] = None,
    scheduled_time: Optional[Union[int, "datetime", "timedelta"]] = None
) -> None:
    """
    Encapsulates the logic of get_backend and sends a message using the appropriate backend.
    
    :param text: The message text to send.
    :param attachment: Optional; Path to the file to attach.
    :param scheduled_time: Optional; Unix timestamp or datetime object for scheduling the message. Or a timedelta with the delay.
    """
    backend = get_backend()
    backend.send_message(
        text=text,
        attachment=attachment,
        scheduled_time=scheduled_time
    )

def send_alert(
        text: Optional[str] = None,
        attachment: Optional[Union[str, "Path"]] = None,
        params: Optional[dict] = None,
        level: Literal["success", "info", "warning", "error"] = "info"
) -> None:
    """
    Send an alert message with the specified text and level.

    :param text: Optional; The message text to send.
    :param attachment: Optional; Path to the file to attach.
    :param params: Optional; Dictionary of parameters to format the text.
    :param level: Optional; The level of the alert message.
    """
    # Get or create the backend instance (always storing it globally)
    backend = get_backend()
    backend.send_alert(
        text=text,
        attachment=attachment,
        params=params,
        level=level
    )


def get_backend(
    alert_token: Optional[str] = None, store: bool = True
) -> "AlertBackend":
    """
    Get or create an AlertBackend instance. If the global backend is None or store is False, initialize it with resolved credentials.

    :param alert_token: Optional; Slack token to override the environment variable.
    :param store: If True, store the backend instance in the global variable.
    :return: An initialized AlertBackend instance.
    """
    global backend

    # Initialize the backend if needed
    if not store or backend is None:
        alert_token, credential_type = resolve_credentials(alert_token)

        if credential_type == "slack":
            from .slack_backend import SlackBackend

            current_backend = SlackBackend(token=alert_token)
        elif credential_type == "telegram":
            from .telegram_backend import TelegramBackend

            current_backend = TelegramBackend(token=alert_token)
        else:
            raise ValueError(f"Unsupported credential type: {credential_type}")

        # Store the backend if required
        if store:
            backend = current_backend
    else:
        # Use the existing backend if already initialized and store is True
        current_backend = backend

    return current_backend


def resolve_credentials(alert_token: Optional[str] = None) -> tuple[str, Literal["slack", "telegram"]]:
    """
    Resolve the credentials for the alert system. Look for environment variables, or use provided overrides.

    :param alert_token: Optional; Slack token to override the environment variable.
    :return: A tuple containing the alert_token and the backend type ('slack').
    """
    alert_token = alert_token or os.getenv(ALERT_TOKEN)

    if not alert_token:
        raise ValueError(
            f"Alert token must be provided or set in the {ALERT_TOKEN} environment variable."
        )
    
    if alert_token.startswith("xoxb-"):
        credential_type = "slack"
    # Check if the token is a Telegram token format
    
    elif len(alert_token.split(":")) == 2:
        credential_type = "telegram"

    return alert_token, credential_type
