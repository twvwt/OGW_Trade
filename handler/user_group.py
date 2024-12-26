from aiogram import F, types, Router
from aiogram import Bot, Dispatcher, types
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaAudio,
                           InputMediaDocument, InputMediaPhoto,
                           InputMediaVideo,FSInputFile, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from string import punctuation
from filters.chat_types import ChatTypeFilter
from database.models import Product, User, BasketItem, News
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'кабан', 'хомяк', 'выхухоль'}
    
current_update = None

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))

async def check_request(update):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        callback_data='request',
        text='✅ПОДТВЕРДИТЬ✅'
    )
    user_id = update.from_user.id
    await update.bot.send_message(user_id, "Пожалуйста, подтвердите свое вступление в группу, нажав на кнопку ниже:", reply_markup=keyboard.as_markup())
    
 
@user_group_router.chat_join_request()
async def start1(update: types.ChatJoinRequest, state: FSMContext):
    global current_update
    current_update = update
    await check_request(update)
    
@router.callback_query(F.data == 'request')
async def process_news_backward_command(callback: CallbackQuery, state: FSMContext):
    global current_update
    await callback.message.answer('Ваша заявка успешно принята! Нажмите /start для начала работы')
    await current_update.approve()
    
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.username}, соблюдайте порядок в чате!')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
