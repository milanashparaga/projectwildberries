from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from Keyboards.keyboard import in_admin, no_add
from create_bot import bot, CHAT
from database.db import db


def validate_user_status(user_status):
    if user_status == "left":
        return False
    if user_status == "canceled":
        return False
    else:
        return True


class FSMSpam(StatesGroup):
    text = State()


async def add_admin(message: types.Message):
    """Команда вызова админ панели"""
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=message.from_user.id)
    if validate_user_status(user_status['status']):
        await bot.send_message(message.from_user.id,
                               "Опять работа((((\n"
                               "Выбери что делаем",
                               reply_markup=in_admin)


async def spam_start(callback_query: types.CallbackQuery):
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=callback_query.from_user.id)
    if validate_user_status(user_status['status']):
        await bot.send_message(callback_query.from_user.id,
                               'Введите текст рассылки или фото для рассылки',
                               reply_markup=no_add)
        await FSMSpam.text.set()
        await callback_query.answer(cache_time=3)


async def spam_finish(message: types.Message, state: FSMContext):
    user_status = await bot.get_chat_member(chat_id=CHAT,
                                            user_id=message.from_user.id)
    if validate_user_status(user_status['status']):
        if message.content_type == 'photo':
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            for ret in db.spam():
                try:
                    await bot.send_photo(chat_id=ret[0],
                                         photo=data['photo'])
                except Exception as e:
                    print(e)
                    continue
        if message.content_type == 'text':
            async with state.proxy() as data:
                data['text'] = message.text
            for ret in db.spam():
                try:
                    await bot.send_message(chat_id=ret[0],
                                           text=data['text'])
                except Exception as e:
                    print(e)
                    continue
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Рассылка успешно завершина')


def register_message_admin(dp: Dispatcher):
    dp.register_message_handler(add_admin,
                                commands=['admin'])
    dp.register_callback_query_handler(spam_start,
                                       text='spam')
    dp.register_message_handler(spam_finish,
                                content_types=['photo', 'text'],
                                state=FSMSpam.text)
