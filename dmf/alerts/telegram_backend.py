import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

try: # Compatibility with Python 3.6+
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

try:
    import requests
except ImportError:
    raise ImportError("The 'requests' package is required to use the Telegram backend."
                        "You can install it with 'pip install dmf-utils[alerts]'.")

from .backend import AlertBackend, AlertException

__all__ = ["TelegramBackend"]

DEFAULT_CHANNEL_ENV = "DMF_DEFAULT_CHANNEL"
TELEGRAM_API_URL = "https://api.telegram.org/bot"

TELEGRAM_EMOJI_MAPPING = {
    ":white_check_mark:": "✅",
    ":books:": "📚",
    ":warning:": "⚠️",
    ":red_circle:": "🔴",
    ":calendar: ": "📅",
    ":bell:": "🔔",
    ":stopwatch: Duration": "⏱️",
    ":inbox_tray:": "📥",
    ":outbox_tray:": "📤",
}


class TelegramBackend(AlertBackend):
    def __init__(
        self, token: str, channel: Optional[str] = None, fail_silently: bool = True
    ):
        """
        Initialize the Telegram backend with the token and default channel (chat ID).
        """
        super().__init__(fail_silently=fail_silently)
        self.token = token
        self.channel = channel or os.getenv(DEFAULT_CHANNEL_ENV)

        if not self.channel:
            raise AlertException(
                "Channel (chat ID) must be provided or set in the DMF_DEFAULT_CHANNEL environment variable."
            )

    def send_message(
        self,
        text: str = "",
        attachment: Optional[Union[str, Path]] = None,
        scheduled_time: Optional[Union[int, datetime]] = None,
    ) -> None:
        """
        Send a message to a Telegram channel, optionally with a file attachment.
        If both attachment and scheduled_time are provided, scheduling is ignored and the message is sent immediately.
        Raises AlertException if an error occurs.
        """
        if scheduled_time is not None:
            if not self.fail_silently:
                raise AlertException(
                    "Scheduled time is provided but is not supported by the Telegram backend."
                )
            logging.warning(
                "Scheduled time is provided but is not supported by the Telegram backend. "
            )

        try:
            self._send_message(text=text, attachment=attachment)
        except Exception as error:
            raise AlertException(f"Error sending message: {str(error)}") from error

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} channel={self.channel}>"

    def _send_message(self, text: str, attachment: Union[str, Path]) -> None:
        """Send a simple message to Telegram."""
        url = f"{TELEGRAM_API_URL}{self.token}/sendMessage"
        data = {
            "chat_id": self.channel,
            "text": text,
            "parse_mode": "Markdown",
        }
        response = requests.post(url, data=data)
        response.raise_for_status()

        if attachment:
            self._send_attachment(attachment)

    def _send_attachment(self, attachment: Union[str, Path]) -> None:
        """Send a message with an attachment to Telegram."""
        file_path = str(attachment)  # Ensure the path is a string
        url = f"{TELEGRAM_API_URL}{self.token}/sendDocument"
        with open(file_path, "rb") as file:
            data = {
                "chat_id": self.channel,
            }
            files = {"document": file}
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()

    def get_alert_text(
        self,
        text: Optional[str] = None,
        level: Literal["success", "info", "warning", "error"] = "info",
        params: Optional[dict] = None,
        separator: str = "\n  • ",
    ) -> str:
        text = super().get_alert_text(text, level, params, separator)

        for emoji, symbol in TELEGRAM_EMOJI_MAPPING.items():
            text = text.replace(emoji, symbol)
        
        return text
