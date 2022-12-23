from time import sleep

from telegram.ext import Updater, CommandHandler
import requests

WEBSITE = 'https://example.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                  'Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"}

TELEGRAM_TOKEN = '<YOUR-TOKEN>'  # follow https://core.telegram.org/bots/tutorial


def start(update, context) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hello world! Type /track <url> to start tracking a url")


def track(update, context):
    check_webpage(update, context)


def check_webpage(update, context):
    website = context.args[0] if context.args else WEBSITE
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
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    start_handler = CommandHandler('start', start)
    track_handler = CommandHandler('track', track, pass_args=True)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(track_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()
