import requests
import json
from datetime import datetime

def send_to_discord(webhook_url, title, description, status, instance, error=None):
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
        'error': 16711680,  # Red
        'warning': 16776960,  # Yellow
        'info': 8421504  # Grey
    }.get(status, 8421504)

    if error:
        description += "\n```" + error + "```"

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    description += f'\nError occurred at **{current_time}** UTC on instance **{instance}**'

    data = {
        "embeds": [{
            "title": error + " - " + instance,
            "description": description,
            "color": color
        }]
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    if response.status_code != 204:
        raise ValueError(f'Request to Discord returned an error {response.status_code}, the response is:\n{response.text}')

webhook_url = "https://discord.com/api/webhooks/1221788278823456778/oFzcgjAQ04KWAAR-gD2O2rI0nDYy4zEKSm_dAiowyW-DKT_aluHHIj8G0Wx_9cUwFX8-"
title = "Error"
description = "An error occurred in a taker instance.\n Please check the logs for more information. \n\nFor more advanced information, check the error message below :\n"
status = "error"
instance = "N/A"
error = "No error given. Please check the logs for more information."
send_to_discord(webhook_url, title, description, status, instance, error)


