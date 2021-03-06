"""Telegram bot for getting Cartola FC tips with Azure function."""

import logging
import os

import azure.functions as func
import requests
import telegram

ALGORITHM = "genetic"
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
    if not os.environ["TELEGRAM_TOKEN"]:
        logging.error("The TELEGRAM_TOKEN must be set")
        raise NotImplementedError

    return telegram.Bot(os.environ["TELEGRAM_TOKEN"])


def is_number(value):
    """Check if string is a number."""
    if value is None:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def format_answer(data):
    """Format answer with squad will be sent to the user."""
    players = sorted(data["players"], key=lambda x: POS_ORDER[x["position"]])
    players_str = "\n".join(
        [
            f"{POS_MAP[row['position']]}  "
            f"{row['name']}  "
            f"({row['club_name']})  "
            f"C${row['price']}"
            for row in players
        ]
    )

    bench = sorted(data["bench"], key=lambda x: POS_ORDER[x["position"]])
    bench_str = "\n".join(
        [
            f"{POS_MAP[row['position']]}  "
            f"{row['name']}  "
            f"({row['club_name']})  "
            f"C${row['price']}"
            for row in bench
        ]
    )
    return f"Titulares:\n{players_str}\n\nBanco de Reservas:\n{bench_str}"


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
            text=f"Fala {name}! Quantas cartoletas voc?? est?? disposto a gastar?",
        )
        return func.HttpResponse(status_code=200)

    if price <= 0:
        bot.sendMessage(
            chat_id=chat_id,
            text=f"{price} n??o ?? uma quantidade v??lida. Preciso de um n??mero positivo.",
        )
        return func.HttpResponse(status_code=200)

    # Shows that the bot is typing to let user know that it is working.
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    res = requests.get(
        url=os.environ["PALPITEIRO_API_URL"],
        params={
            "code": os.environ["PALPITEIRO_API_KEY"],
            "price": price,
            "scheme": "433x",
            "algorithm": ALGORITHM,
            "max_players_per_club": 5,
        },
    )

    if res.status_code != 200:
        bot.sendMessage(
            chat_id=chat_id,
            text=(
                "Aconteceu algo inesperado =(. "
                "Voc?? poderia mandar um print para @matheusdocouto?"
            ),
        )
        return func.HttpResponse(status_code=200)

    bot.sendMessage(chat_id=chat_id, text=format_answer(res.json()))
    return func.HttpResponse(status_code=200)
