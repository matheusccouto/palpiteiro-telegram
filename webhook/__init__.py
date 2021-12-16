"""Telegram bot for getting Cartola FC tips with Azure function."""

import logging
import os

import azure.functions as func
import requests
import telegram

ALGORITHM = "greedy"
POS_MAP = {
    "goalkeeper": "GOL",
    "fullback": "LAT",
    "defender": "ZAG",
    "midfielder": "MEI",
    "forward": "ATA",
    "coach": "TEC",
}
POS_ORDER = {
    "goalkeeper": 1,
    "fullback": 2,
    "defender": 3,
    "midfielder": 4,
    "forward": 5,
    "coach": 6,
}


class MessageError(Exception):
    """Error that indicates that there is an error on the message."""


def configure_telegram():
    """
    Configures the bot with a Telegram Token.

    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    if not TELEGRAM_TOKEN:
        logging.error("The TELEGRAM_TOKEN must be set")
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)


def is_number(string):
    """Check if string is a number."""
    try:
        float(string)
        return True
    except ValueError:
        return False


def format_answer(data):
    """Format answer with squad will be sent to the user."""
    data = sorted(data, key=lambda x: POS_ORDER[x["position"]])
    return "\n".join(
        [
            f"{POS_MAP[row['position']]}  "
            f"{row['name']}  "
            f"({row['club_name']})  "
            f"C${row['price']}"
            for row in data
        ]
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Runs the Telegram webhook."""
    bot = configure_telegram()

    update = telegram.Update.de_json(req.get_json(), bot)
    chat_id = update.effective_message.chat.id
    text = update.effective_message.text
    name = update.effective_message.chat.first_name

    if is_number(text):
        price = float(text)
    else:
        bot.sendMessage(
            chat_id=chat_id,
            text=f"Fala {name}! Quantas cartoletas você está disposto a gastar?",
        )
        return func.HttpResponse("Success", status_code=200)

    if price <= 0:
        bot.sendMessage(
            chat_id=chat_id,
            text=f"{price} não é uma quantidade válida. Preciso de um número positivo.",
        )
        return func.HttpResponse("Success", status_code=200)

    # Shows that the bot is typing to let user know that it is working.
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    res = requests.get(
        url=os.environ["PALPITEIRO_API_URL"],
        params={
            "code": os.environ["PALPITEIRO_API_KEY"],
            "price": str(price),
            "scheme": "442",
            "algorithm": ALGORITHM,
        },
    )

    bot.sendMessage(chat_id=chat_id, text=format_answer(res.json()))
    return func.HttpResponse("Success", status_code=200)
