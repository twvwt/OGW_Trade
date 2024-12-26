import json

from aiogram import Bot, Dispatcher, types
from aiogram import F, types, Router
from aiogram.filters import or_f, Command, CommandStart, StateFilter
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaAudio,
                           InputMediaDocument, InputMediaPhoto,
                           InputMediaVideo,FSInputFile, Message)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from database.orm_query import orm_add_BasketItem
from database.models import Product, User, BasketItem, News
from filters.chat_types import ChatTypeFilter
from filters.help_filter import orm_put_category, orm_put_postcategory, orm_put_products_by_postcategory, get_or_create_user
from lexicon.lexicon import LEXICON_RU, LEXICON_COMMANDS_RU, LEXICON_PAGINATION_RU, LEXICON_DELYVERY_RU
from keyboard.keyboard_help import create_inline_kb
import config
user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

category = {}
subcategory = {}

#Машины состояний
class PersonalAccount(StatesGroup):
    name = State()
    first_name = State()
    adress = State()
    delivery = State()
    payment = State()
    texts = {
        'PersonalAccount:name': 'Введите заново свое имя',
        'PersonalAccount:first_name': 'Введите заново свое фамилие',
        'PersonalAccount:adress': 'Введите заново свой адрес',
        'PersonalAccount:delivery': 'Введите заново удобный способ доставки',
        'PersonalAccount:payment': 'Введите заново удобный способ оплаты'
    }
    
# Определяем состояния
class MenuStates(StatesGroup):
    main_menu = State()
    basket_menu = State()
    category_menu = State()
    subcategory_menu = State()
    product_menu = State()
    category_key = State()
    subcategory_key = State()
    subcategory_callback = State()
    subcategory_name = State()
    product_dict = State()
    page: int
    
    

# async def add_to_cart(callback: types.CallbackQuery, session: AsyncSession):
#     user = callback.from_user
#     await orm_add_user(
#         session,
#         user_id=user.id,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         phone=None,
#     )
#     await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
#     await callback.answer("Товар добавлен в корзину.")

@user_private_router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession):
    user_id = message.from_user.id
    print(user_id)
    first_name = message.from_user.first_name
    print(first_name)
    last_name = message.from_user.last_name
    print(last_name)

    user, created = await get_or_create_user(session, user_id, first_name, last_name)
    await message.answer(LEXICON_RU['/start'])

@user_private_router.message(or_f(Command('menu'),F.text.lower() == 'меню'))
async def process_menu_command(message: Message, state: FSMContext):
    await state.set_state(MenuStates.main_menu)
    text = '🍏Розничная и оптовая продажа, ремонт техники Apple🍏\n\nПриобрести технику или записаться на ремон / Trade-in'
    await message.answer_photo(
        photo=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text,
        reply_markup=create_inline_kb(
            2,
            catalog = LEXICON_COMMANDS_RU['catalog'],
            news = LEXICON_COMMANDS_RU['news'],
            basket_buyer = LEXICON_COMMANDS_RU['basket_buyer'],
            orders = LEXICON_COMMANDS_RU['orders'],
            personal_account = LEXICON_COMMANDS_RU['personal_account'],
            search = LEXICON_COMMANDS_RU['search'],
            support = LEXICON_COMMANDS_RU['support']
        )
    )
async def process_menu_refresh_command(message: Message, state: FSMContext):
    await state.set_state(MenuStates.main_menu)
    text = '🍏Розничная и оптовая продажа, ремонт техники Apple🍏\n\nПриобрести технику или записаться на ремон / Trade-in'
    media = InputMediaPhoto(
        media=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text
    )
    await message.edit_media(
        media = media,
        reply_markup=create_inline_kb(
            2,
            catalog = LEXICON_COMMANDS_RU['catalog'],
            news = LEXICON_COMMANDS_RU['news'],
            basket_buyer = LEXICON_COMMANDS_RU['basket_buyer'],
            orders = LEXICON_COMMANDS_RU['orders'],
            personal_account = LEXICON_COMMANDS_RU['personal_account'],
            search = LEXICON_COMMANDS_RU['search'],
            support = LEXICON_COMMANDS_RU['support']
        )
    )
    
@user_private_router.callback_query(F.data == 'catalog')
async def process_category_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(MenuStates.category_menu)
    text = 'Выберите категорию'
    
    # Создаем объект InputMediaPhoto с файлом изображения
    media = InputMediaPhoto(
        media=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text
    )
    keyboard = InlineKeyboardBuilder()
    
    # Получаем категории
    category = await orm_put_category(session)
    
    for key, value in category.items():
        # Добавляем информацию о категории в callback_data
        keyboard.button(text=f'💠{value}💠', callback_data=f'category_{key}')
    
    keyboard.button(
        callback_data='search',
        text=LEXICON_COMMANDS_RU['search']
    )
    keyboard.button(
        callback_data='support',
        text=LEXICON_COMMANDS_RU['support']
    )
    keyboard.button(
        callback_data='back1',
        text=LEXICON_RU['back']
    )
    keyboard.adjust(2)
    reply_markup_category = keyboard.as_markup()
    
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup_category
    )


@user_private_router.callback_query(F.data.startswith('category_'))
async def process_subcategory_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(MenuStates.subcategory_menu)
    # Извлекаем номер категории из callback_data
    category_key = callback.data.split('_')[-1]
    await state.update_data(category_key=category_key)
    config.product_path.append(category_key)
    # Получаем подкатегории для выбранной категории
    category_name, subcategory = await orm_put_postcategory(session, category_key)
    
    text = f'Вашему вниманию предоставляется большой выбор ассортимента {category_name}, выберите, какую именно модель вы бы хотели?'
    media = InputMediaPhoto(
        media=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text
    )
    keyboard = InlineKeyboardBuilder()
    
    for key, value in subcategory.items():
        keyboard.button(text=f'💠{value}💠', callback_data=key)
    
    keyboard.button(
        callback_data='search',
        text=LEXICON_COMMANDS_RU['search']
    )
    keyboard.button(
        callback_data='support',
        text=LEXICON_COMMANDS_RU['support']
    )
    keyboard.button(
        callback_data='back1',
        text=LEXICON_RU['back']
    )
    keyboard.adjust(2)
    reply_markup_subcategory = keyboard.as_markup()
    
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup_subcategory
    )
    return subcategory

@user_private_router.callback_query(F.data.startswith('postcategory_'))
async def process_product_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(MenuStates.product_menu)
    postcategory_key = callback.data.split('_')[-1]
    await state.update_data(postcategory_key=postcategory_key)
    data = await state.get_data()
    category_key = data.get('category_key')
    subcategory_name, product_dict = await orm_put_products_by_postcategory(session, category_key, postcategory_key)
    await state.update_data(page=0)
    await state.update_data(product_dict = product_dict)
    await state.update_data(subcategory_name = subcategory_name)
    
    await update_product_message(callback, product_dict, subcategory_name, state, page = 0)


@user_private_router.callback_query(F.data == 'backward')
async def process_backward_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')  # Извлекаем текущее значение page, по умолчанию 0
    if page > 0:  # Проверяем, чтобы не было отрицательной страницы
        await state.update_data(page=page - 1)  # Уменьшаем значение page
        page = page - 1
    else:
        await callback.answer('Меньше некуда, это первая страниц!')
    data = await state.get_data()  # Обновляем данные
    postcategory_key = data['postcategory_key']
    category_key = data.get('category_key')
    subcategory_name = data.get('subcategory_name')
    product_dict = data.get('product_dict')
    await update_product_message(callback, product_dict, subcategory_name, state, page)


@user_private_router.callback_query(F.data == 'forward')
async def process_forward_command(callback: CallbackQuery, session: AsyncSession,  state: FSMContext):
    data = await state.get_data()
    page = data.get('page')  # Извлекаем текущее значение page
    # Получаем количество товаров
    product_dict = data.get('product_dict', {})
    if page < len(product_dict) - 1:  # Проверяем, чтобы не выйти за пределы
        await state.update_data(page=page + 1)  # Увеличиваем значение page
        page = page +1
    else:
        await callback.answer('Дальше некуда,это последняя страница!')
    data = await state.get_data()  # Обновляем данные
    postcategory_key = data['postcategory_key']
    category_key = data.get('category_key')
    subcategory_name = data.get('subcategory_name')
    product_dict = data.get('product_dict')
    
    await update_product_message(callback, product_dict, subcategory_name, state, page)



async def update_product_message(callback: CallbackQuery, product_dict, subcategory_name, state: FSMContext, page):
    print(subcategory_name)
    text = f'Вашему вниманию предоставляется большой выбор ассортимента {subcategory_name}, выберите необходимую вам модель'
    if 'iphone' in subcategory_name:
        path = ''
    media = InputMediaPhoto(
        media=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text)
    
    keyboard_product = InlineKeyboardBuilder()
    
    if f'product_{page}' in product_dict:
        button1 = InlineKeyboardButton(text=product_dict[f'product_{page}']['name'], callback_data='button_1')
        button2 = InlineKeyboardButton(text=f'Цена: {int(product_dict[f"product_{page}"]["price"])} ₽', callback_data='buy')
    else:
        button1 = InlineKeyboardButton(text='-----------', callback_data='no_product')
        button2 = InlineKeyboardButton(text='-----------', callback_data='no_product')

    button3 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['backward'], callback_data='backward')
    button4 = InlineKeyboardButton(text=f'{page+1}/{len(product_dict)}', callback_data='pagenation')
    button5 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['forward'], callback_data='forward')
    button6 = InlineKeyboardButton(text=LEXICON_RU['back'], callback_data='back1')

    # Строим клавиатуру
    keyboard_product.row(button1)
    keyboard_product.row(button2)
    keyboard_product.row(button3, button4, button5)
    keyboard_product.row(button6)
    
    reply_markup_product = keyboard_product.as_markup()
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup_product
    )

@user_private_router.callback_query(F.data == 'button_1')
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')
    product_dict = data.get('product_dict')
    await callback.answer(product_dict[f'product_{page}']['name'])
    
@user_private_router.callback_query(F.data == 'button_2')
async def process_admin_price_command(message: Message, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')
    product_dict = data.get('product_list')
    await message.answer(product_dict[page]['name'])

@user_private_router.callback_query(or_f(F.data == 'personal_account', F.text.lower() == 'личный кабинет'))
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    user_items = await session.execute(
        select(User).where(User.user_id == user_id)
    )
    user_items = user_items.scalars().first()  # Получаем все элементы пользователя
    summ_price = 0
    if user_items:
        print('True')
        first_name = user_items.first_name
        last_name = user_items.last_name
        address = user_items.address
        delivery_method = user_items.delivery_method
        payment_method = user_items.payment_method
        await callback.message.answer(
            text=(
                f'Ваши данные:\n\n'
                f'Фамилия: {last_name}\n'
                f'Имя: {first_name}\n'
                f'Адрес: {address}\n'
                f'Вид доставки: {delivery_method}\n'
                f'Вид оплаты: {payment_method}\n\n'
                'Если хотите изменить ваши данные, воспользуйтесь кнопкой ниже:'
            ),
            reply_markup=create_inline_kb(
                1,
                edit_personal_account='Изменить данные'
            ))
    else:
        print('False')
        await callback.message.answer(
            text = f'Вы еще не идентифицированы в нашей базе\nПройдите регистрацию по кнопке ниже:',
            reply_markup=create_inline_kb(
                1,
                edit_personal_account = 'Изменить данные'
            ))
#Хэндлеры для заполнения данных личного кабинета
@user_private_router.callback_query(F.data == 'edit_personal_account')
async def process_client_name_command(callback: CallbackQuery, state: FSMContext): 
    await callback.message.answer(
        text = 'Введите ваше имя:',
        reply_markup=create_inline_kb(
            1,
            cancellation = LEXICON_RU['cancellation']
        ))
    await state.set_state(PersonalAccount.name)
    
@user_private_router.message(PersonalAccount.name, F.text)
async def process_client_first_name_command(message: Message,state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text = 'Введите вашу фамилию:',
        reply_markup=create_inline_kb(
            2,
            back = LEXICON_RU['back'],
            cancellation = LEXICON_RU['cancellation']
        ))
    await state.set_state(PersonalAccount.first_name)
    
@user_private_router.message(PersonalAccount.adress,F.text)
async def process_client_delivery_command(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    await message.answer(
        text = f'Выберите способ доставки:\n{LEXICON_DELYVERY_RU['standart_delivery']}\n{LEXICON_DELYVERY_RU['shop_delivery']}\n{LEXICON_DELYVERY_RU['curyer_delivery']}',
        reply_markup=create_inline_kb(
            2,
            back = LEXICON_RU['back'],
            cancellation = LEXICON_RU['cancellation']
        ))
    await state.set_state(PersonalAccount.delivery)
    
@user_private_router.message(PersonalAccount.delivery,F.text)
async def process_client_payment_command(message: Message, state: FSMContext):
    await state.update_data(delivery=message.text)
    await message.answer(
        text = f'Выберите способ оплаты:\n{LEXICON_DELYVERY_RU['standart_delivery']}\n\n{LEXICON_DELYVERY_RU['shop_delivery']}', 
        reply_markup=create_inline_kb(
            2,
            back = LEXICON_RU['back'],
            cancellation = LEXICON_RU['cancellation']
        ))

    await state.set_state(PersonalAccount.payment)
    
@user_private_router.message(PersonalAccount.payment, F.text)
async def finalize_account_update(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(payment=message.text)

    # Получаем данные из состояния
    data = await state.get_data()
    user_id = message.from_user.id

    # Обновляем данные в базе данных, используя переданную сессию
    stmt = (
        update(User).
        where(User.user_id == user_id).
        values(
            first_name=data.get('name'), 
            last_name=data.get('first_name'), 
            address=data.get('address'), 
            delivery_method=data.get('delivery'), 
            payment_method=data.get('payment')
        )
    )
    
    await session.execute(stmt)  # Выполнение запроса
    await session.commit()  # Фиксация изменений

    
    text = '🍏Розничная и оптовая продажа, ремонт техники Apple🍏\n\nПриобрести технику или записаться на ремон / Trade-in'
    await message.answer_photo(
        photo=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text,
        reply_markup=create_inline_kb(
            2,
            catalog = LEXICON_COMMANDS_RU['catalog'],
            news = LEXICON_COMMANDS_RU['news'],
            basket_buyer = LEXICON_COMMANDS_RU['basket_buyer'],
            orders = LEXICON_COMMANDS_RU['orders'],
            personal_account = LEXICON_COMMANDS_RU['personal_account'],
            search = LEXICON_COMMANDS_RU['search'],
            support = LEXICON_COMMANDS_RU['support']
        )
    )
    person_data = await state.get_data()
    await state.clear()

@user_private_router.message(PersonalAccount.payment)
async def process_client_payment_command(message: Message, state: FSMContext):
    await message.answer(
        text = 'Что-то пошло не так, попробуйте заново')

@user_private_router.message(PersonalAccount.first_name,F.text)
async def process_client_adress_command(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(
        text = 'Введите ваш адрес:',
        reply_markup=create_inline_kb(
            2,
            back = LEXICON_RU['back'],
            cancellation = LEXICON_RU['cancellation']
        ))
    await state.set_state(PersonalAccount.adress)
    
@user_private_router.callback_query(StateFilter('*'), or_f(F.data == 'back', F.text.lower() == 'назад'))
async def process_admin_price_command(callback: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == PersonalAccount.name:
        pass
    pervious = None
    for step in PersonalAccount.__all_states__:
        if step.state == current_state:
            await state.set_state(pervious)
            await callback.message.answer(PersonalAccount.texts[pervious.state])
            return
        pervious = step
    
# Обработчик кнопки "Назад"
@user_private_router.callback_query(F.data == 'back1')
async def process_back_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    current_state = await state.get_state()
    if current_state == MenuStates.product_menu.state:
        # Возвращаемся к меню категорий
        await process_category_command(callback, session, state)
        
    elif current_state == MenuStates.subcategory_menu.state:
        # Возвращаемся к меню категорий
        await process_category_command(callback, session, state)
        
    elif current_state == MenuStates.category_menu.state:
        # Возвращаемся в главное меню
        await process_menu_refresh_command(callback.message, state)
    elif current_state == MenuStates.basket_menu.state:
        # Возвращаемся в главное меню
        await process_menu_refresh_command(callback.message, state)
    else:
        await process_menu_refresh_command(callback.message, state)
        

@user_private_router.callback_query(StateFilter('*'), or_f(F.data == 'cancellation', F.text.lower() == 'отмена'))
async def process_admin_price_command(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.answer('Действия отменены')
    text = '🍏Розничная и оптовая продажа, ремонт техники Apple🍏\n\nПриобрести технику или записаться на ремон / Trade-in'
    await callback.message.answer_photo(
        photo=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text,
        reply_markup=create_inline_kb(
            2,
            catalog = LEXICON_COMMANDS_RU['catalog'],
            news = LEXICON_COMMANDS_RU['news'],
            basket_buyer = LEXICON_COMMANDS_RU['basket_buyer'],
            orders = LEXICON_COMMANDS_RU['orders'],
            personal_account = LEXICON_COMMANDS_RU['personal_account'],
            search = LEXICON_COMMANDS_RU['search'],
            support = LEXICON_COMMANDS_RU['support']
        )
    )
    
@user_private_router.callback_query(or_f(F.data == 'support', F.text.lower() == 'поддержка'))
async def process_admin_price_command(callback: types.CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    user_items = await session.execute(
        select(User).where(User.user_id == user_id)
    )
    user_items = user_items.scalars().first()  # Получаем все элементы пользователя
    print(user_items)
    summ_price = 0
    
    # Инициализация переменной text
    text = "Данные пользователя недоступны."  # Сообщение по умолчанию, если user_items равно None

    if user_items:
        first_name = user_items.first_name
        last_name = user_items.last_name
        address = user_items.address
        delivery_method = user_items.delivery_method
        payment_method = user_items.payment_method
        text = (
            f'Данные пользователя:\n\n'
            f'Фамилия: {last_name}\n'
            f'Имя: {first_name}\n'
            f'Адрес: {address}\n'
            f'Вид доставки: {delivery_method}\n'
            f'Вид оплаты: {payment_method}\n'
        )
    
    await callback.answer('Мы оповестили менеджеров службы поддержки\nВ скором времени они с вами свяжутся')
    bot: Bot = callback.bot
    # Отправка сообщения в другой чат
    await bot.send_message(chat_id=-1002446526769, text=f"/support\nhttps://t.me/{callback.from_user.username}\n{text}")

@user_private_router.callback_query(F.data == 'buy')
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession):
    product = callback.message.reply_markup.inline_keyboard[0][0].text
    user_id = callback.from_user.id

    # Извлекаем существующий элемент корзины для данного пользователя
    basket_item = await session.execute(
        select(BasketItem).where(BasketItem.user_id == user_id)
    )
    basket_item = basket_item.scalar_one_or_none()  # Получаем объект или None

    if basket_item:
        # Если корзина существует, обновляем продукт
        products = json.loads(basket_item.product_name)  # Десериализуем строку JSON в словарь

        # Увеличиваем количество, если продукт уже есть, или добавляем новый
        if product in products:
            products[product] += 1
        else:
            products[product] = 1  # Добавляем новый продукт с количеством 1
        # Сериализуем словарь обратно в строку JSON перед сохранением
        basket_item.product_name = json.dumps(products)
        await session.commit()
    else:
        # Если корзина не существует, создаем новую запись
        new_basket_item = BasketItem(user_id=user_id, product_name=json.dumps({product: 1}))  # Начальное количество 1
        session.add(new_basket_item)
        await session.commit()

    # Отправляем ответ пользователю
    await callback.answer(f"Товар '{product}' добавлен в вашу корзину.")



@user_private_router.callback_query(or_f(F.data == 'basket_buyer', F.text.lower() == 'корзина'))
async def process_basket_buyer_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(MenuStates.basket_menu)
    user_id = callback.from_user.id

    # Извлекаем корзину для данного пользователя
    basket_items = await session.execute(
        select(BasketItem).where(BasketItem.user_id == user_id)
    )
    basket_items = basket_items.scalars().all()  # Получаем все элементы корзины

    response_message = "Ваша корзина:\n"
    summ_price = 0
    if basket_items:
        for item in basket_items:
            products = json.loads(item.product_name)  # Десериализуем строку JSON в словарь
            print(products)
            for product_name, quantity in products.items():
                # Извлекаем информацию о продукте
                product_query = await session.execute(
                    select(Product).where(Product.name == product_name)
                )
                product = product_query.scalars().first()  # Используем first() вместо scalar_one_or_none()
                print(f'Товар: {product}')
                if product:
                    # Добавляем информацию о товаре в сообщение
                    response_message += (
                        f"{product.name} (Цена: {int(product.new_price)} ₽.)\n"
                    )
                    summ_price += int(product.new_price)
                else:
                    response_message += f"{product_name} (информация о продукте недоступна)\n"
            response_message += f'\n Итоговая стоимость: {summ_price} ₽'

    else:
        response_message = "Ваша корзина пуста"
    
    media = InputMediaPhoto(
        media=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=response_message)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        callback_data='buy_products',
        text='Заказать'
    )
    keyboard.button(
        callback_data='back1',
        text=LEXICON_RU['back']
    )
    keyboard.button(
        callback_data='delete_basket',
        text = '❌Очистить корзину❌'
    )
    keyboard.adjust(2)
    reply_markup_basket = keyboard.as_markup()
    
    # Отправляем сообщение пользователю
    if response_message != 'Ваша корзина пуста':
        await callback.message.edit_media(
            media=media,
            reply_markup=reply_markup_basket
        )
    else:
        await callback.answer('Ваша корзина пуста!')

@user_private_router.callback_query(F.data == 'delete_basket')
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    user_id = callback.from_user.id
    await session.execute(delete(BasketItem).where(BasketItem.user_id == user_id))
    await session.commit()
    await callback.answer('Ваша корзина очищена!')
    await process_back_command(callback, session, state)
    
@user_private_router.callback_query(F.data == 'buy_products')
async def process_admin_price_command(callback: CallbackQuery, session: AsyncSession):
    await callback.answer('Мы оповестили наших менеджеров, скоро с вами свяжутся для оформления заказа')
    user_id = callback.from_user.id
    
    # Извлекаем корзину для данного пользователя
    basket_items = await session.execute(
        select(BasketItem).where(BasketItem.user_id == user_id)
    )
    basket_items = basket_items.scalars().all()  # Получаем все элементы корзины
    
    response_message = "Корзина покупателя:\n"
    summ_price = 0
    
    if basket_items:
        for item in basket_items:
            products = json.loads(item.product_name)  # Десериализуем строку JSON в словарь
            print(products)
            for product_name, quantity in products.items():
                # Извлекаем информацию о продукте
                product_query = await session.execute(
                    select(Product).where(Product.name == product_name)
                )
                product = product_query.scalars().first()  # Используем first() для безопасного получения
                
                print(f'Товар: {product}')
                if product:
                    # Добавляем информацию о товаре в сообщение
                    response_message += (
                        f"{product.name} (Цена: {int(product.new_price)} ₽.)\n"
                    )
                    summ_price += int(product.new_price) * quantity  # Учитываем количество
                else:
                    response_message += f"{product_name} (информация о продукте недоступна)\n"
        
        response_message += f'\n Итоговая стоимость: {summ_price} ₽'
    
    # Извлекаем данные пользователя
    user_items = await session.execute(
        select(User).where(User.user_id == user_id)
    )
    user_items = user_items.scalars().first()  # Получаем первого пользователя
    
    print(user_items)
    
    if user_items:
        first_name = user_items.first_name
        last_name = user_items.last_name
        address = user_items.address
        delivery_method = user_items.delivery_method
        payment_method = user_items.payment_method
        
        text = (
            f'Данные пользователя:\n\n'
            f'Фамилия: {last_name}\n'
            f'Имя: {first_name}\n'
            f'Адрес: {address}\n'
            f'Вид доставки: {delivery_method}\n'
            f'Вид оплаты: {payment_method}\n'
        )
    
    bot: Bot = callback.bot
    # Отправка сообщения в другой чат
    await bot.send_message(chat_id=-1002248889896, text=f"/ПОКУПАТЕЛЬ\nhttps://t.me/{callback.from_user.username}\n{text}\n{response_message}")
    
@user_private_router.callback_query(or_f(F.data == 'orders', F.text.lower() == 'заказы'))
async def process_admin_price_command(message: Message):
    await message.answer('Вы все еще не сделали ни одного заказа!')
    
class Form(StatesGroup):
    search = State()
    page: int
    
    
@user_private_router.callback_query(or_f(F.data == 'search', F.text.lower() == 'поиск определенного товара'))
async def process_admin_price_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Пожалуйста, напишите запрос для поиска продукта.')
    await state.set_state(Form.search)
# Обработка текста запроса
@user_private_router.message(Form.search, F.text)
async def process_client_search_command(message: Message, session: AsyncSession, state: FSMContext):
    query = message.text
    result = await session.execute(select(Product).where(Product.name.ilike(f'%{query}%')))
    products = result.scalars().all()
    
    products_list = [
        {
            'name': product.name,
            'price': product.price,
            'description': product.description
        }
        for product in products
    ]
    
    await state.update_data(product_list=products_list)
    await state.update_data(page=0)
    await update_search_product(message, products_list, state, page=0)

async def update_search_product(message: Message, product_list, state: FSMContext, page):
    text = f'По вашему запросу найдено {len(product_list)} товаров'
    media = InputMediaPhoto(
        media=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
        caption=text
    )
    
    keyboard_product = InlineKeyboardBuilder()
    
    if len(product_list) > 0:
        button1 = InlineKeyboardButton(text=product_list[page]['name'], callback_data='button_2')
        button2 = InlineKeyboardButton(text=f'Цена: {int(product_list[page]["price"])} ₽', callback_data='buy')
    else:
        button1 = InlineKeyboardButton(text='-----------', callback_data='no_product')
        button2 = InlineKeyboardButton(text='-----------', callback_data='no_product')

    button3 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['backward'], callback_data='backward_search')
    button4 = InlineKeyboardButton(text=f'{page + 1}/{len(product_list)}', callback_data='pagination')
    button5 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['forward'], callback_data='forward_search')
    button6 = InlineKeyboardButton(text=LEXICON_RU['back'], callback_data='back1')

    # Строим клавиатуру
    keyboard_product.row(button1)
    keyboard_product.row(button2)
    keyboard_product.row(button3, button4, button5)
    keyboard_product.row(button6)
    
    reply_markup_product = keyboard_product.as_markup()
    if page == 0:
        await message.answer_photo(
            photo=FSInputFile('photo_2024-11-18_02-47-25.jpg'),
            caption=text, 
            reply_markup=reply_markup_product
            )
    else:
        await message.edit_media(
            media=media,
            reply_markup=reply_markup_product
        )

@user_private_router.callback_query(F.data == 'backward_search')
async def process_backward_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')  # Извлекаем текущее значение page, по умолчанию 0
    if page > 0:  # Проверяем, чтобы не было отрицательной страницы
        await state.update_data(page=page - 1)  # Уменьшаем значение page
        page = page - 1
    else:
        await callback.answer('Меньше некуда, это первая страниц!')
    data = await state.get_data()  # Обновляем данные
    product_list = data.get('product_list')
    await update_search_product(callback.message, product_list, state, page)


@user_private_router.callback_query(F.data == 'forward_search')
async def process_forward_command(callback: CallbackQuery, session: AsyncSession,  state: FSMContext):
    data = await state.get_data()
    page = data.get('page')  # Извлекаем текущее значение page
    # Получаем количество товаров
    product_dict = data.get('product_list', {})
    if page < len(product_dict) - 1:  # Проверяем, чтобы не выйти за пределы
        await state.update_data(page=page + 1)  # Увеличиваем значение page
        page = page +1
    else:
        await callback.answer('Дальше некуда,это последняя страница!')
    data = await state.get_data()  # Обновляем данные
    product_list = data.get('product_list')
    
    await update_search_product(callback.message, product_list, state, page)
    
    
class NewsCaption(StatesGroup):
    page:int
    
    
@user_private_router.callback_query(F.data == 'news')
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
    new_list = sorted(new_list, key=lambda d: d['created'], reverse=True)
    print(new_list[0])
    await state.update_data(news_list=new_list)
    await state.update_data(page=0)
    await update_news(callback, new_list, state, page=0)   




@user_private_router.callback_query(F.data == 'news_backward')
async def process_news_backward_command(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')  # Извлекаем текущее значение page, по умолчанию 0
    if page > 0:  # Проверяем, чтобы не было отрицательной страницы
        await state.update_data(page=page - 1)  # Уменьшаем значение page
        page = page - 1
    else:
        await callback.answer('Меньше некуда, это первая страниц!')
    data = await state.get_data()  # Обновляем данные
    new_list = data['news_list']
    await update_news(callback, new_list, state, page)


@user_private_router.callback_query(F.data == 'news_forward')
async def process_news_forward_command(callback: CallbackQuery, session: AsyncSession,  state: FSMContext):
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
    await update_news(callback, new_list, state, page)


# ,
async def update_news(callback: CallbackQuery, new_list, state: FSMContext, page):
    keyboard_product = InlineKeyboardBuilder()
    media = InputMediaPhoto(
        media=new_list[page]['photo_id'],
        caption=f'Дата актуальности:   {new_list[page]['created']}\n\n{new_list[page]['news_text']}'
    )
    button3 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['backward'], callback_data='news_backward')
    button4 = InlineKeyboardButton(text=f'{page+1}/{len(new_list)}', callback_data='pagenation')
    button5 = InlineKeyboardButton(text=LEXICON_PAGINATION_RU['forward'], callback_data='news_forward')
    button6 = InlineKeyboardButton(text=LEXICON_RU['back'], callback_data='back1')

    # Строим клавиатуру

    keyboard_product.row(button3, button4, button5)
    keyboard_product.row(button6)
    
    reply_markup_product = keyboard_product.as_markup()
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup_product
    )

