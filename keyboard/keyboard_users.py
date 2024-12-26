from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU, LEXICON_COMMANDS_RU
from keyboard.keyboard_help import create_inline_kb


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://nasyrov07i:ogwtradetrade@shop.ci2tl.mongodb.net/?retryWrites=true&w=majority&appName=shop"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Функция для формирования инлайн-клавиатуры на лету


def create_category():
    category_osn = {}
    db = client.shop
    coll = db.products
    category = coll.distinct('category')
    for i in range(len(category)):
        category_osn[f'category_{i}'] = category[i]
        
    return category_osn

def create_subcategory(number):
    subcategory_osn = {}
    subcategory = set()
    db = client.shop
    coll = db.products
    category = coll.distinct('category')
    guery = {"category": category[int(number)]}
    for value in coll.find(guery, {'_id': 0, "postcategory" : 1}):
        subcategory.add(value['postcategory'])
    for i in range(len(list(subcategory))):
        subcategory_osn[f'subcategory_{i}'] = list(subcategory)[i]
    return subcategory_osn

def create_product(subcategory):
    product_osn = {}
    product = set()
    db = client.shop
    coll = db.products
    category = coll.distinct('category')
    guery = {'postcategory': subcategory}
    for value in coll.find(guery, {'_id': 0, "name" : 1, "new_price":1}):
        product.append({value['name'] : value['new_price']})
    for i in range(len(list(product))):
        product_osn[f'product_{i}'] = list(product)[i]
        
#     return product_osn
# # Функция, генерирующая клавиатуру для страницы книги
# def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
#     # Инициализируем билдер
#     kb_builder = InlineKeyboardBuilder()
#     # Добавляем в билдер ряд с кнопками
#     kb_builder.row(*[InlineKeyboardButton(
#         text=LEXICON[button] if button in LEXICON else button,
#         callback_data=button) for button in buttons]
#     )
#     # Возвращаем объект инлайн-клавиатуры
#     return kb_builder.as_markup()
