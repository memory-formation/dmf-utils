import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .backend import AlertBackend, AlertException

__all__ = ["SlackBackend"]

DEFAULT_CHANNEL_ENV = "DMF_DEFAULT_CHANNEL"

class SlackBackend(AlertBackend):
    def __init__(self, token: str, channel: Optional[str] = None, fail_silently: bool = True):
        """
        Initialize the Slack backend with the token and default channel.
        """
        super().__init__(fail_silently=fail_silently)
        self.client = WebClient(token=token)
        self.channel = channel or os.getenv(DEFAULT_CHANNEL_ENV)

    def send_message(
        self,
        text: str = "",
        attachment: Optional[Union[str, Path]] = None,
        scheduled_time: Optional[Union[int, datetime]] = None,
    ) -> None:
        """
        Send a message to a Slack channel, optionally with a file attachment or scheduled time.
        Raises AlertException if an error occurs, or if both attachment and scheduled_time are provided.
        """
        if attachment and scheduled_time:
            raise AlertException("Cannot send a message with both an attachment and a scheduled time.")

        try:
            if scheduled_time:
                self._send_scheduled_message(text, self.channel, scheduled_time)
            elif attachment:
                self._send_attachment_message(text, self.channel, attachment)
            else:
                self._send_message(text, self.channel)
        except SlackApiError as error:
            if self.fail_silently:
                logging.error(f"Error sending message: {error.response['error']}")
            else:
                raise AlertException(f"Error sending message: {error.response['error']}") from error

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} channel={self.channel}>"

    def _send_scheduled_message(self, text: str, channel: str, post_at: Union[int, "datetime", "timedelta"]) -> dict:
        """Send a scheduled message to Slack."""

        # Convert timedelta to Unix timestamp if needed
        if isinstance(post_at, timedelta):
            post_at = int((datetime.now() + post_at).timestamp())

        # Convert datetime to Unix timestamp if needed
        if isinstance(post_at, datetime):
            post_at = int(post_at.timestamp())

        return self.client.chat_scheduleMessage(
            channel=channel,
            text=text,
            post_at=post_at
        )

    def _send_attachment_message(self, text: str, channel: str, attachment: Union[str, Path]) -> dict:
        """Send a message with an attachment to Slack."""
        file_path = str(attachment)  # Ensure the path is a string
        return self.client.files_upload_v2(
            channel=channel,
            file=file_path,
            initial_comment=text
        )

    def _send_message(self, text: str, channel: str) -> dict:
        """Send a simple message to Slack."""
        return self.client.chat_postMessage(
            channel=channel,
            text=text
        )
