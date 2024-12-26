import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from aiogram.filters import BaseFilter
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, or_f
from aiogram.types import Message
import config
BOT_TOKEN = '6572426542:AAH5ZqallMMWzPJSWTFMJzHMBxWrCEltJN4'

chanel_id =  -1001751731925
        
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
    
    
    
# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем логгер
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

chat_admins = []
admin_ids = []
async def fetch_chat_administrators(channel_id):
    chat_admins = await bot.get_chat_administrators(channel_id)
    for admin in chat_admins:
        config.admin_ids.append(admin.user.id)

# Создаем клавиатуру
url_button_1 = InlineKeyboardButton(
    text='КУПИТЬ',
    url='https://t.me/odil552558'
)
keyboard = InlineKeyboardMarkup(inline_keyboard=[[url_button_1]])


# @dp.message(IsAdmin(admin_ids))
async def process_start_command(message: Message):
    await message.answer('Привет! Я предназначен для публикации постов в канал.\nНапиши мне слово "Публикация" для начала создавания поста!')
    await fetch_chat_administrators(chanel_id)
    
@dp.message(or_f(IsAdmin(config.admin_ids), F.text.lower() == 'Публикация'))
async def send_photo_echo(message: Message):
    print(config.admin_ids)
    await message.answer('Привет, адмминистратор, отправьте нам пост, который вы хотите опубликовать в вашем канале!')
    # Проверяем, есть ли фото и подпись
    if message.photo:
        # Получаем самое большое фото
        photo = message.photo[-1]
        # Получаем подпись, если она есть
        caption = message.caption if message.caption else "Фото без подписи"
        
        # Отправляем фото с подписью
        await bot.send_photo(chat_id=-1002053500771, photo=photo.file_id, caption=caption, reply_markup=keyboard)
    
    # Конфигурируем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
            '[%(asctime)s] - %(name)s - %(message)s')

# Выводим в консоль информацию о начале запуска бота
logger.info('Starting bot')

dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(send_photo_echo, F.photo)

if __name__ == '__main__':
    
    dp.run_polling(bot)
