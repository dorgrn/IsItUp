import os
from time import sleep

import dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

"""
IsItUp.
    Bot that checks polls until a website is up and let's you know when it does!
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                  'Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"}


def start(update, context) -> None:
    """
    Callback that iterates the bot's options.
    :param update: represents an incoming update.
    :param context: context object passed to the callback
    :return: None
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hello world! Type /track <url> to start tracking a url")


def check_webpage(update: Update, context: CallbackContext) -> None:
    """
    Callback that polls until a website is up (returns 200).
    :param update: represents an incoming update.
    :param context: context object passed to the callback
    :return: None
    """
    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Please supply website to track\n/track <url>')
        return

    website = context.args[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Starting to poll for website {website}')

    try:
        response = requests.get(website, headers=headers)

        while response.status_code == 404:
            print(f"response code was {response.status_code}")
            sleep(3600)
            response = requests.get(website, headers=headers)

        if response.status_code == 200:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Webpage {website} is up!')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Failed polling for {website}. Error is: {response.status_code}: {response.text}')
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Failed polling for {website}. Error is: {e}')


def main() -> None:
    dotenv.load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')  # to get token, follow https://core.telegram.org/bots/tutorial
    if not telegram_token or telegram_token == "<YOUR_TELEGRAM_TOKEN>":
        raise ValueError('Please define\nTELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN>\nvariable in .env file')

    updater = Updater(token=telegram_token, use_context=True)

    start_handler = CommandHandler('start', start)
    track_handler = CommandHandler('track', check_webpage, pass_args=True)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(track_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()
