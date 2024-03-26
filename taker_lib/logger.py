##
## Conseil Junior Taker - 2024
## mp [Ubuntu:22.04]
## File description:
## taker instance library for taker logging operations
## @julesreyn
##

import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

log = logging.getLogger(__name__)


load_dotenv()
desc_exemple = "An error occurred on a taker instance.\n Please check the logs for more information. \n\nFor more advanced information, check the error message below :\n"
error_exemple = "No error given. Please check the logs for more information."


def logger(description=desc_exemple, status="error", instance="N/A", error=error_exemple):
    """
    Send a message to a Discord channel via a webhook.

    Args:
        webhook_url (str): The URL of the Discord webhook.
        title (str): The title of the message.
        description (str): The description of the message.
        status (str): The status of the message, can be 'error', 'warning', or 'info'.
        error (str): The error message to display in a code block.
    """
    color = {
        'critical': 16711680,  # Red
        'error': 16711680,  # Red
        'warning': 16776960,  # Yellow
        'info': 8421504  # Grey
    }.get(status, 8421504)

    if error:
        description += f"\n```{error}```"

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    description += f'\nError occurred at **{current_time}** UTC on instance **{instance}**'
    getattr(log, status)(f'{error} - {instance}')
    data = {
        "embeds": [{
            "title": f"{error} - {instance}",
            "description": description,
            "color": color
        }]
    }

    response = requests.post(os.getenv('WEBHOOK_URL'), data=json.dumps(data), headers={"Content-Type": "application/json"})
    log.info(f'Sent message to Discord with status code {response.status_code}')
    if response.status_code != 204:
        raise ValueError(f'Request to Discord returned an error {response.status_code}, the response is:\n{response.text}')
