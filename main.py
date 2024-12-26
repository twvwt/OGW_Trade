import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from middlewares.db import DataBaseSession

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from database.engine import create_db, drop_db, session_maker

from handler.user_private import user_private_router
from handler.user_group import user_group_router, router
from handler.admin_private import admin_private_router
# from common.bot_cmd_list import private

ALLOWED_UPDATES = ['message', 'edited_message']

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем логгер
logger = logging.getLogger(__name__)

async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')
    

# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config

    # Инициализируем бот и диспетчер
    bot = Bot(token= os.getenv('TOKEN'),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()


    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    # admin_private_router.message.middleware(C)
    # Настраиваем главное меню бота
    # await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(admin_private_router)
    dp.include_router(user_group_router)
    dp.include_router(user_private_router)
    dp.include_router(router)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())