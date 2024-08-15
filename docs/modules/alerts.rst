Alerts
======

The Alerts module in DMF Utils provides tools for sending notifications and alerts via messaging services such as Slack and Telegram. These alerts can be used to notify when a function completes, send files, or schedule messages. The module is highly configurable and designed to integrate into your existing workflows.

To install this module, use the following command:

.. code-block:: bash

    pip install dmf-utils[alerts]

Overview
--------

The Alerts module allows you to:

- Send messages and files to Slack or Telegram.
- Decorate functions to automatically send notifications when they finish executing.
- Customize alerts with different levels such as `success`, `info`, `warning`, and `error`.
- Use different backends (Slack, Telegram) with simple configuration.

This module is useful for integrating notifications into your data processing pipelines, experiments, or any long-running tasks where you need to be informed of the status or results.

Reference
---------

**Main Functions**:

The main functions provided by the Alerts module are:

.. autosummary::
   :toctree: autosummary

   dmf.alerts.alert
   dmf.alerts.send_alert
   dmf.alerts.send_message

**Backends**:

Internally, the Alerts module uses different backends to send messages to Slack or Telegram, transparently handling the communication with the messaging services. See configuration instructions below for setting up Slack or Telegram.

.. autosummary::
   :toctree: autosummary

   dmf.alerts.get_backend
   dmf.alerts.slack_backend.SlackBackend
   dmf.alerts.telegram_backend.TelegramBackend

**Other**:

Additional classes and exceptions used by the module:

.. autosummary::
   :toctree: autosummary

   dmf.alerts.backend.AlertException
   dmf.alerts.backend.AlertBackend

Configuration
-------------

Setting Up Slack
~~~~~~~~~~~~~~~~

To use the Alerts module with Slack, follow these steps:

1. Go to the `Slack Apps website <https://api.slack.com/apps>`_ and log in to your workspace.
2. Go to an existing app or create a new Slack app in your workspace. If you are part of the DMF, you can ask for our API keys.
3. Navigate to the "OAuth & Permissions" section in your app's settings.
4. In the "Scopes" section, add the following scopes:
   - `chat:write` (to send messages)
   - `files:write` (to send files)
   - `channels:read` (to write in public channels without being invited)
5. Install the app in a channel. This can be a personal app or any channel where you want to send notifications.
6. If you want to send notifications to a private channel, invite the bot to the channel. You can do this with the command ``/invite @name_of_the_bot``.

To use the functions without specifying credentials every time:

7. Save the token into the environment variable ``DMF_ALERTS_TOKEN``:

   .. code-block:: bash

       export DMF_ALERTS_TOKEN="your-slack-api-token"

8. Save the channel name or the channel ID into the environment variable ``DMF_DEFAULT_CHANNEL``:

   .. code-block:: bash

       export DMF_DEFAULT_CHANNEL="your-channel-name-or-id"

Once these steps are complete, your Slack app will be able to send alerts through the DMF Utils package without requiring you to specify the token or channel name in your code.

Setting Up Telegram
~~~~~~~~~~~~~~~~~~~

To use the Alerts module with Telegram, follow these steps:

1. Open Telegram and start a chat with the `BotFather <https://t.me/BotFather>`_, which is the official bot used to create and manage Telegram bots.
2. Create a new bot by sending the command ``/newbot`` to the BotFather. Follow the prompts to choose a name and username for your bot. Once the bot is created, the BotFather will provide you with an API token.
3. Save the API token provided by the BotFather. This token is required to authenticate your bot and send messages.
4. Obtain the chat ID where the bot will send messages. You can get the chat ID by adding your bot to a group and sending a message. Then, use the ``https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`` with your bot token to retrieve the chat ID from the response.

   Replace `<YOUR_BOT_TOKEN>` with your actual bot token in the API call.

   Alternatively, you can use third-party tools or Telegram bot management tools to easily find the chat ID.

To use the functions without specifying credentials every time:

5. Save the bot token into the environment variable ``DMF_ALERTS_TOKEN``:

   .. code-block:: bash

       export DMF_ALERTS_TOKEN="your-telegram-bot-token"

6. Save the chat ID into the environment variable ``DMF_DEFAULT_CHANNEL``:

   .. code-block:: bash

       export DMF_DEFAULT_CHANNEL="your-chat-id"

Once these steps are complete, your Telegram bot will be able to send alerts through the DMF Utils package without requiring you to specify the token or chat ID in your code.

Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~

The Alerts module also provides a command-line tool called `dmf-alert` for sending messages directly from the terminal.

**Example**:

.. code-block:: bash

    dmf-alert "Execution finished successfully" -a output.txt

This command will send a message saying "Execution finished successfully" and attach the file `output.txt`.

Alternatively, you can use it to return the output of a command:

.. code-block:: bash

    ./my_script | dmf-alert -l info

Examples
--------

Sending Alerts in Python
~~~~~~~~~~~~~~~~~~~~~~~~

You can send alerts directly from your Python code using the `send_alert` and `send_message` functions.

**Example**:

.. code-block:: python

    from dmf.alerts import send_alert

    send_alert(text="This is a test alert", level="info")

This will send a simple alert with the specified text and level.

Function Decorator
~~~~~~~~~~~~~~~~~~

The `alert` decorator can be used to automatically send notifications when a function completes. This is particularly useful for long-running tasks.

**Example**:

.. code-block:: python

    from dmf.alerts import alert

    @alert
    def my_function(name):
        # Simulate a task
        sleep(5)
        return f"Hello, {name}!"

    my_function("World")

In this example, a notification will be sent when `my_function` finishes, including the function's output and duration.

Sending Messages with Attachments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also send files as attachments in your alerts. This is useful for sending logs, reports, or any other file generated during your script's execution.

**Example**:

.. code-block:: python

    from dmf.alerts import send_message
    from pathlib import Path

    send_message(text="Here is the report", attachment=Path("report.pdf"))

This will send the `report.pdf` file along with the message text.
