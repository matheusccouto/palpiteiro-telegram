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
    logger.info("Message received: %s", req.get_json())

    bot = configure_telegram()

    body = req.get_json()
    logger.info("Body: %s", body)
    update = telegram.Update.de_json(body, bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        text = "Hello, human!"

    bot.sendMessage(chat_id=chat_id, text=text)
    logger.info("Message sent")

    return func.HttpResponse(
        json.dumps(text),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
