import config

from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.utils.executor import start_webhook

from aiogram.types import InputFile

import qrcode

# webhook settings
WEBHOOK_HOST = 'https://lenichev.ru'
WEBHOOK_PATH = config.path
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = config.port


bot = Bot(token=config.token)
dp = Dispatcher(bot)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    #logging.warning('Shutting down..')
    await bot.delete_webhook()
    #logging.warning('Bye!')


async def qrcode_simple_text(text, output_png):
    img = qrcode.make(text)
    img.save(output_png)


@dp.message_handler(commands=['start'])
async def start(msg):
    pass


@dp.message_handler(content_types=['text'])
async def text_def(msg):
    name = 'qrcodes/' + str(msg['from']['id']) + '.jpeg'
    await qrcode_simple_text(msg.text, name)
    photo = InputFile(name)

    await bot.send_photo(msg['from']['id'], photo)



if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
