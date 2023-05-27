from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Keyboards.keyboard import in_choise_start, phone_contact, in_no_ad, in_choise_bonus, in_choise_back, in_back_main
from create_bot import bot, dp, CHAT


class FSMReport(StatesGroup):
    photo = State()
    phone = State()


async def coomand_start(message: types.Message):
    """Хендлер старт и хелп"""
    await bot.send_message(message.from_user.id, 'Здравствуйте!\n'
                                                 'На связи служба заботы Wildberries\n'
                                                 'Спасибо что выбрали именно нас!🌺\n'
                                                 'В данном боте Вы можете:\n'
                                                 '1.Решить любой вопрос, связанный с вашим заказом.\n'
                                                 '2.Оставить отзыв и получить бонус.\n'
                                                 '<b>Пожалуйста выберите что хотите сделать:</b>',
                           reply_markup=in_choise_start)


async def main_menu(callback: types.CallbackQuery):
    """Хендлер для команды старт по кнопке назад"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Здравствуйте!\n'
                                          'На связи служба заботы Wildberries\n'
                                          'Спасибо что выбрали именно нас!🌺\n'
                                          'В данном боте Вы можете:\n'
                                          '1.Решить любой вопрос, связанный с вашим заказом.\n'
                                          '2.Оставить отзыв и получить бонус.\n'
                                          '<b>Пожалуйста выберите что хотите сделать:</b>',
                                     reply_markup=in_choise_start)


async def want_donus(callback: types.CallbackQuery):
    """Хендлер бонусов"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Мы очень рады, что товар Вам понравился😍\n'
                                          'Выберите, какой отзыв вы хотите оставить?',
                                     reply_markup=in_choise_bonus)


async def get_bonus_start(callback: types.CallbackQuery):
    await FSMReport.photo.set()
    await bot.send_message(callback.from_user.id,
                           text='Пожалуйста загрузите скриншот вашего отзыва',
                           reply_markup=InlineKeyboardMarkup().add(in_no_ad))


async def add_report_photo(message: types.Message, state: FSMContext):
    """Ловим картинку от пользователя"""
    async with state.proxy() as data:
        data['name'] = message.from_user.first_name
        data['photo'] = message.photo[0].file_id
    await FSMReport.next()
    await bot.send_message(message.from_user.id,
                           'Отлично, теперь укажите номер телефона.\n'
                            'Просто нажмите кнопку внизу',
                           reply_markup=phone_contact)


async def add_to_report_phone(message: types.Message, state: FSMContext):
    """Ловим номер телефона и отправляем данные админу"""
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
    await bot.send_photo(chat_id=CHAT,
                         photo=data['photo'])
    await bot.send_message(chat_id=CHAT,
                           text=f"Пользователь {data['name']}\n"
                                              f"Оставил отзыв и хочет бонус.\n"
                                              f"Номер телефона:{data['phone']}",
                           reply_markup=InlineKeyboardMarkup().
                           add(InlineKeyboardButton('❗ Связаться',
                                                    url=f'https://t.me/{message.from_user.username}')))
    await state.finish()
    await bot.send_message(message.contact.user_id, 'Отлично!!!!\n'
                                                    'Как только проверим ваш отзыв,'
                                                    'бонусы сразу будут начисленны на ваш телефон',
                           reply_markup=InlineKeyboardMarkup().add(in_back_main))


async def get_50(callback: types.CallbackQuery):
    """Хендлер(инструкция), чтобы получить бонус """
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Инструкция:\n'
                                          '1.Нажмите на кнопку ниже и пройдите'
                                          'по ссылке на страницу купленного товара\n'
                                          '2.Оставьте текстовый отзыв \n'
                                          '3.После того, как отзыв будет опубликован - '
                                          'пришлите фото подтверждение (или скриншот отзыва),\n'
                                          'вернитесь в предыдущее меню и нажмите кнопку -\n'
                                          '"💰 Я уже оставил отзыв, хочу бонус"',
                                     reply_markup=in_choise_back)


async def get_75(callback: types.CallbackQuery):
    """Хендлер(инструкция), чтобы получить бонус """
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Инструкция:\n'
                                          '1.Нажмите на кнопку ниже и пройдите'
                                          'по ссылке на страницу купленного товара\n'
                                          '2.Оставьте фото отзыв \n'
                                          '3.После того, как отзыв будет опубликован - '
                                          'пришлите фото подтверждение (или скриншот отзыва),\n'
                                          'вернитесь в предыдущее меню и нажмите кнопку -\n'
                                          '"💰 Я уже оставил отзыв, хочу бонус"',
                                     reply_markup=in_choise_back)


async def cancel(callback: types.CallbackQuery, state: FSMContext):
    """Отмена действий"""
    await state.finish()
    await bot.answer_callback_query(callback.id,
                                    text='Отменил')


def register_message_other(dp: dp):
    """Регистрация хендлеров"""
    dp.register_message_handler(coomand_start,
                                commands=['start', 'help'])
    dp.register_callback_query_handler(main_menu,
                                       text='main')
    dp.register_callback_query_handler(want_donus,
                                       text='bonus')
    dp.register_callback_query_handler(get_bonus_start,
                                       text='get_bonus',
                                       state=None)
    dp.register_message_handler(add_report_photo,
                                content_types=['photo'],
                                state=FSMReport.photo)
    dp.register_message_handler(add_to_report_phone,
                                content_types=types.ContentType.CONTACT,
                                state=FSMReport.phone)
    dp.register_callback_query_handler(cancel,
                                       text='no',
                                       state="*")
    dp.register_callback_query_handler(get_50,
                                       text='50')
    dp.register_callback_query_handler(get_75,
                                       text='75')
