import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Register
router = Router()


@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer('Привет', reply_markup = kb.main)


@router.message(Command('help'))
async def cmd_help(message:Message):
    await message.answer('Вы нажали на кнопку помощи')

@router.message(F.text == 'Каталог')
async def catalog(message:Message):
    await message.answer('Выберите категорию товара', reply_markup = kb.catalog)

@router.callback_query(F.data == 't-shirts')
async def t_shirt(callback:CallbackQuery):
    await callback.answer('Вы выбрали категорию футболки', show_alert=True)
    await callback.message.answer('Вы выбрали катгорию футболки')


@router.message(Command('register'))
async def  register(message:Message, state:FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя: ')

@router.message(Register.name)
async def register_name(message:Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@router.message(Register.age)
async def register_age(message:Message, state: FSMContext):
    await state.update_data(age = message.text)
    await state.set_state(Register.phone)
    await message.answer('Введите ваш номер телефона', reply_markup = kb.get_number)


@router.message(Register.phone, F.contact)
async def register_phone(message:Message, state:FSMContext):
    await state.update_data(phone = message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data['name']}\n Ваш возраст: {data['age']}\n Ваш номер {data['phone']}')
    await state.clear()