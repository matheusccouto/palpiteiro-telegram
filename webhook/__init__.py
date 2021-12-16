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


def extract_price(text):
    """Extract price from text."""
    try:
        price = float(text)
    except ValueError:
        return func.HttpResponse(
            f"Text should be a number representing the price, but received {text}.",
            status_code=400,
        )

    if price <= 0:
        return func.HttpResponse(
            f"Price should be positive, but received {text}.",
            status_code=400,
        )

    return price


def extract_scheme(text):
    """Extract price from text."""
    return "442"  # FIXME To be developed


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
    print(req.get_json())
    bot = configure_telegram()
    bot.sendMessage(chat_id=163127655, text="It works")
    return func.HttpResponse("Success", status_code=200)


# def main(req: func.HttpRequest) -> func.HttpResponse:
#     """Runs the Telegram webhook."""
#     body = req.get_json()
#     logging.info("Message received: %s", body)

#     bot = configure_telegram()

#     update = telegram.Update.de_json(body, bot)
#     chat_id = update.effective_message.chat.id
#     text = update.effective_message.text

#     if text == "/start":
#         bot.sendMessage(chat_id=chat_id, text="Até quanto você está disposto a pagar?")
#         return func.HttpResponse("Success", status_code=200)

#     # Shows that the bot is typing to let user know that it is working.
#     bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

#     res = requests.get(
#         url=os.environ["PALPITEIRO_API_URL"],
#         params={
#             "code": os.environ["PALPITEIRO_API_KEY"],
#             "price": extract_price(text),
#             "scheme": extract_scheme(text),
#             "algorithm": ALGORITHM,
#         },
#     )

#     answer = format_answer(res.json())

#     bot.sendMessage(chat_id=chat_id, text=answer)
#     logging.info("Message sent to ID %s: %s", chat_id, answer)

#     return func.HttpResponse("Success", status_code=200)
