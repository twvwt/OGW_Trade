import os
import json
import io
import pandas as pd
import openpyxl


from aiogram import Bot, F, types, Router
from aiogram.filters import or_f, Command, CommandStart
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaAudio,
                           InputMediaDocument, InputMediaPhoto,
                           InputMediaVideo,FSInputFile, Message, InputFile)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select

from filters.chat_types import ChatTypeFilter, IsAdmin
from lexicon.lexicon import LEXICON_RU, LEXICON_COMMANDS_RU, LEXICON_PAGINATION_RU
from keyboard.keyboard_help import create_inline_kb
from database.models import Product, News, User
from database.orm_query import orm_add_product



admin_private_router = Router()

class Form(StatesGroup):
    waiting_for_news_text = State()
    waiting_for_news_date = State()

admin_private_router.message.filter(ChatTypeFilter(['private']), IsAdmin())
@admin_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(LEXICON_RU['/start'])
    
@admin_private_router.message(or_f(Command('admin'),F.text.lower() == 'админка'))
async def process_admin_menu_command(message: Message):
    text = 'Вы авторизованы как администратор, что хотите изменить?'
    await message.answer(
        text= text,
        reply_markup=create_inline_kb(
            2,
            dowload_price = 'Посмотреть таблицу цен',
            buyer_users = 'Посмотреть список пользователей ботом',
            message_other = 'Разослать сообщение пользователям бота',
            refresh_price = 'Обновить данные о ценах',
            add_news = 'Добавить новость',
            replace_news = 'Новости'
        )
    )

@admin_private_router.callback_query(or_f(F.data == 'refresh_price', F.text.lower() == 'прайс'))
async def process_admin_price_command(message: Message, session: AsyncSession):
    stmt = delete(Product)
    await session.execute(stmt)
    await session.commit()
    with open('data.json', 'r', encoding="utf-8") as file:
        product = json.load(file)
    for item in product:
        await orm_add_product(session, item)
    await message.answer('Таблица обновлена')
    
    
@admin_private_router.callback_query(or_f(F.data == 'dowload_price', F.text.lower() == 'Товары'))
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession):
    await callback.answer('Выгружаем таблицу с товарами...')
    stmt = select(Product)
    result = await session.execute(stmt)
    data = result.scalars().all()

    # Преобразуем данные в DataFrame без использования to_dict
    df = pd.DataFrame([{
        "id": item.id,
        "category": item.category,
        "postcategory": item.postcategory,
        "name": item.name,
        "price": item.price,
        "new_price": item.new_price,
    } for item in data])

    print(df)
    filename = 'data_products.xlsx'
    df.to_excel(filename, index=False)
    with open(filename, 'rb') as file:
        await callback.message.answer_document(FSInputFile(filename))

    await callback.answer('Таблица пользователей успешно выгружена!')


@admin_private_router.callback_query(or_f(F.data == 'buyer_users', F.text.lower() == 'пользователи'))
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession):
    await callback.answer('Выгружаем таблицу пользователей...')
    stmt = select(User)
    result = await session.execute(stmt)
    data = result.scalars().all()

    # Преобразуем данные в DataFrame без использования to_dict
    df = pd.DataFrame([{
        "id": item.id,
        "user_id": item.user_id,
        "first_name": item.first_name,
        "last_name": item.last_name,
        "address": item.address,
        "delivery_method": item.delivery_method,
        "payment_method": item.payment_method,
    } for item in data])

    print(df)
    filename = 'data_users.xlsx'
    df.to_excel(filename, index=False)
    with open(filename, 'rb') as file:
        await callback.message.answer_document(FSInputFile(filename))

    await callback.answer('Таблица пользователей успешно выгружена!')

class BroadcastState:
    waiting_for_photo = False
    waiting_for_description = False
    photo = None
    description = None

broadcast_state = {}

@admin_private_router.callback_query(or_f(F.data == 'message_other', F.text.lower() == 'рассылка'))
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession):
    admin_id = callback.from_user.id
    broadcast_state[admin_id] = BroadcastState()
    
    await callback.answer('Пожалуйста, отправьте фотографию для рассылки.')
    broadcast_state[admin_id].waiting_for_photo = True

@admin_private_router.message(F.photo & F.from_user.id)
async def handle_photo(message: types.Message):
    admin_id = message.from_user.id

    if admin_id in broadcast_state and broadcast_state[admin_id].waiting_for_photo:
        broadcast_state[admin_id].photo = message.photo[-1].file_id  # Получаем наилучшее качество фото
        broadcast_state[admin_id].waiting_for_photo = False
        broadcast_state[admin_id].waiting_for_description = True
        
        await message.reply('Фотография получена. Пожалуйста, введите описание.')
        

@admin_private_router.message(F.text & F.from_user.id)
async def handle_description(message: types.Message, bot: Bot, session: AsyncSession):
    admin_id = message.from_user.id

    if admin_id in broadcast_state and broadcast_state[admin_id].waiting_for_description:
        broadcast_state[admin_id].description = message.text
        photo_id = broadcast_state[admin_id].photo
        description = broadcast_state[admin_id].description
        
        # Получаем всех пользователей из БД
        result = await session.execute(select(User))
        users = result.scalars().all()

        for user in users:
            print(user.user_id)
            print(user.last_name)
            try:
                await message.bot.send_photo(chat_id=user.user_id, photo=photo_id, caption=description)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user.user_id}: {e}")

        await message.reply('Рассылка завершена!')
        del broadcast_state[admin_id]  # Удаляем состояние после завершения рассылки












































#Управление новостями
class NewsForm(StatesGroup):
    waiting_for_photo = State()
    waiting_for_description = State()
    
@admin_private_router.callback_query(F.data == 'add_news')
async def start_add_news(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, отправьте фото для новости.")
    await state.set_state(NewsForm.waiting_for_photo)
    
@admin_private_router.message(NewsForm.waiting_for_photo)
async def process_photo(message: types.Message, state: FSMContext):
    if message.photo:
        # Сохраняем фото (можно сохранить в файловую систему или в облачное хранилище)
        photo_id = message.photo[-1].file_id  # Получаем ID самого большого фото
        await state.update_data(photo_id=photo_id)  # Сохраняем ID фото в состоянии

        await message.answer("Отправьте описание новости.")
        await state.set_state(NewsForm.waiting_for_description)
    else:
        await message.answer("Пожалуйста, отправьте фото.")

@admin_private_router.message(NewsForm.waiting_for_description)
async def process_description(message: types.Message, session: AsyncSession, state: FSMContext):
    description = message.text  # Получаем текст описания
    data = await state.get_data()  # Получаем сохраненные данные
    photo_id = data.get('photo_id')  # Извлекаем ID фото

    # Сохраняем новость в БД
    new_news = News(news_text=description, photo_id=photo_id)  # Предположим, что у вас есть поле photo_id
    session.add(new_news)
    await session.commit()
    await message.answer("Новость успешно добавлена!")
    
class NewsCaption(StatesGroup):
    page:int
    
    
@admin_private_router.callback_query(F.data == 'replace_news')
async def send_news(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
        # Извлекаем все новости из базы данных
    result = await session.execute(select(News))
    news_list = result.scalars().all()  # Получаем все новости
    new_list = [
    {
        'photo_id': new.photo_id,
        'news_text': new.news_text,
        'created':new.created
    }
    for new in news_list
    ]
    print(new_list[0])
    await state.update_data(news_list=new_list)
    await state.update_data(page=0)
    await admin_update_news(callback, new_list, state, page=0)   




@admin_private_router.callback_query(F.data == 'admin_news_backward')
async def admin_news_backward_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')  # Извлекаем текущее значение page, по умолчанию 0
    if page > 0:  # Проверяем, чтобы не было отрицательной страницы
        await state.update_data(page=page - 1)  # Уменьшаем значение page
        page = page - 1
    else:
        await callback.answer('Меньше некуда, это первая страниц!')
    data = await state.get_data()  # Обновляем данные
    new_list = data['news_list']
    await admin_update_news(callback, new_list, state, page)


@admin_private_router.callback_query(F.data == 'admin_news_forward')
async def admin_news_forward_command(callback: CallbackQuery, session: AsyncSession,  state: FSMContext):
    data = await state.get_data()
    page = data.get('page')  # Извлекаем текущее значение page
    # Получаем количество товаров
    print(page)
    news_list = data.get('news_list', {})
    if page < len(news_list) - 1:  # Проверяем, чтобы не выйти за пределы
        await state.update_data(page=page + 1)  # Увеличиваем значение page
        page = page +1
    else:
        await callback.answer('Дальше некуда,это последняя страница!')
    data = await state.get_data()  # Обновляем данные
    new_list = data['news_list']
    await admin_update_news(callback, new_list, state, page)


# ,
async def admin_update_news(callback: CallbackQuery, new_list, state: FSMContext, page):
    keyboard_product = InlineKeyboardBuilder()
    media = InputMediaPhoto(
        media=new_list[page]['photo_id'],
        caption=f'Дата актуальности:   {new_list[page]['created']}\n\n{new_list[page]['news_text']}'
    )
    button3 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['backward'], callback_data='admin_news_backward')
    button4 = InlineKeyboardButton(text=f'{page+1}/{len(new_list)}', callback_data='pagenation')
    button5 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['forward'], callback_data='admin_news_forward')
    button6 = InlineKeyboardButton(text=LEXICON_RU['back'], callback_data='back1')
    button7 = InlineKeyboardButton(text='❌Удалить❌', callback_data='admin_delete_news')

    # Строим клавиатуру

    keyboard_product.row(button3, button4, button5)
    keyboard_product.row(button6)
    keyboard_product.row(button7)
    
    reply_markup_product = keyboard_product.as_markup()
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup_product
    )
    
    
@admin_private_router.callback_query(F.data == 'admin_delete_news')
async def process_delete_news_command(callback: CallbackQuery, session: AsyncSession,  state: FSMContext):
    data = await state.get_data()
    new_list = data.get('news_list')
    page = data.get('page')
    if not new_list or page >= len(new_list):
        await callback.answer("Нет доступных новостей для удаления.")
        return

    # Получаем дату создания текущей новости
    photo_id = new_list[page]['photo_id']
    await session.execute(
        delete(News).where(News.photo_id == photo_id)
    )
    await session.commit()

    # После удаления, обновляем список новостей
    new_list.pop(page)  # Удаляем новость из списка
    await state.update_data(news_list=new_list)

    # Проверяем, остались ли новости
    if new_list:
        # Если остались, обновляем текущую страницу (если она больше, чем количество новостей, уменьшаем ее)
        if page >= len(new_list):
            page = len(new_list) - 1
        await admin_update_news(callback, new_list, state, page)
    else:
        await callback.message.answer("Все новости удалены.")
        await callback.answer()
    