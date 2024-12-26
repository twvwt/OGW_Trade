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






