import asyncio
from gc import callbacks

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Register
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message:Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в наш магазин', reply_markup = kb.main)

@router.message(F.text == 'Контакты')
async def contacts(message:Message):
    await message.answer('Благодарим', reply_markup=kb.whatsapp_button)



@router.message(F.text == 'Каталог')
async def catalog(message:Message):
    await message.answer('Выберите категорию товара', reply_markup = await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def category(callback:CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup = await kb.items(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('item_'))
async def category(callback:CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'название: {item_data.name}\n Описание: {item_data.description}\n Цена: {item_data.price}$\n',
                                  reply_markup = await kb.items(callback.data.split('_')[1]))