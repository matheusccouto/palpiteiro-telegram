"""Azure function."""

import logging
import os

import azure.functions as func
import telegram

import json


# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)


def configure_telegram():
    """
    Configures the bot with a Telegram Token.

    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    if not TELEGRAM_TOKEN:
        logger.error("The TELEGRAM_TOKEN must be set")
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Runs the Telegram webhook."""
    bot = configure_telegram()
    bot.set_webhook(req.url.split("set_webhook")[0] + "webhook")
    return func.HttpResponse(
        json.dumps("Success."),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )