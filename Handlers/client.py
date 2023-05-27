from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, dp, CHAT
from Keyboards.keyboard import in_troble_choise, \
    in_no_ad, phone_contact, in_troble_item, \
    in_back_main, back_main_menu, no_add
from database.db import db
from utils import sale


class FSMTroble(StatesGroup):
    photo = State()
    phone = State()
    description = State()


class FSMBroken(StatesGroup):
    photo = State()
    photo_2 = State()
    phone = State()


class FSMClientRegister(StatesGroup):
    name = State()
    phone_number = State()
    confirm = State()


async def have_toble(callback: types.CallbackQuery):
    """Хендлер подменю 'Проблемы с товаром' """
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Давайте разбираться, в чём проблема',
                                     reply_markup=in_troble_choise)


async def wrong_description(callback: types.CallbackQuery):
    """Переходим в подменю'Проблемы с товаром->Неправильное описание'"""
    await callback.answer(cache_time=3)
    await FSMTroble.photo.set()
    await bot.send_message(callback.from_user.id,
                           'Нам очень жаль😪\nПришлите, пожалуйста, фото несоответствия',
                           reply_markup=InlineKeyboardMarkup().add(in_no_ad)
                           )


async def photo_wrong_description(message: types.Message, state: FSMContext):
    """Ловим фото от пользователя"""
    async with state.proxy() as data:
        data['photo_rep'] = message.photo[0].file_id
    await bot.send_message(message.from_user.id,
                           'Отлично, теперь укажите номер телефона.\nПросто нажмите кнопку внизу',
                           reply_markup=phone_contact
                           )
    await FSMTroble.next()


async def phone_wrong_description(message: types.Message, state: FSMContext):
    """Ловим телефон от пользователя"""
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
    await bot.send_photo(chat_id=CHAT, photo=data['photo_rep'])
    await bot.send_message(
        chat_id=CHAT,
        text=f"Пользователь {message.from_user.username}"
             f"\nЖалуется на несоответсвие описания.\nНомер телефона: {data['phone_number']}",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton('❗ Связаться',
                                 url=f'https://t.me/{message.from_user.username}')
        )
    )
    await bot.send_message(message.from_user.id, 'Я передал всё менеджеру, в скором времени с вами свяжутся',
                           reply_markup=InlineKeyboardMarkup().add(in_back_main))
    await state.finish()


async def troble_item(callback: types.CallbackQuery):
    """Переходим в подменю'Проблемы с товаром->Товар поврежден'"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(
        text='Нам очень жаль!😪\n'
             'Нужно понять, повреждение произошло в момент транспортировки или это заводской брак',
        reply_markup=in_troble_item)


async def trobel_item_start(callback: types.CallbackQuery):
    """Запуск состояний для репорта о повреждении товара"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(
        text='Прикрепите,пожалуйста, фото коробки',
        reply_markup=InlineKeyboardMarkup().add(in_no_ad))
    await FSMBroken.photo.set()


async def trobel_item_box(message: types.Message, state: FSMContext):
    """Ловим фотографии"""
    async with state.proxy() as data:
        data['photo_item'] = message.photo[0].file_id
    await FSMBroken.next()
    await bot.send_message(message.from_user.id, text='Прикрепите,пожалуйста, фото товара',
                           reply_markup=InlineKeyboardMarkup().add(in_no_ad))


async def trobel_item_photo(message: types.Message, state: FSMContext):
    """Ловим фотографии"""
    async with state.proxy() as data:
        data['photo_box'] = message.photo[0].file_id
    await bot.send_message(message.from_user.id,
                           'Отлично, теперь укажите номер телефона.\n'
                           'Просто нажмите кнопку снизу',
                           reply_markup=phone_contact
                           )
    await FSMBroken.next()


async def trobel_item_phone(message: types.Message, state: FSMContext):
    """Ловим номер телефона"""
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
    await bot.send_photo(chat_id=CHAT, photo=data['photo_box'])
    await bot.send_photo(chat_id=CHAT, photo=data['photo_item'])
    await bot.send_message(
        chat_id=CHAT,
        text=f"Пользователь {message.from_user.username}\n"
             f"Жалуется на повреждение товара.\n"
             f"Номер телефона: {data['phone']}",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                '❗ Связаться', url=f'https://t.me/{message.from_user.username}')
        )
    )
    await bot.send_message(message.from_user.id,
                           'Я передал все менеджеру, в скором времени с вами свяжутся',
                           reply_markup=InlineKeyboardMarkup().add(in_back_main))

    await state.finish()


async def get_manger(callback: types.CallbackQuery):
    """Хендлер кнопки связи с менеджером"""
    await callback.answer(cache_time=3)
    await callback.message.edit_text(text='Пожалуйста, опишите вашу проблему',
                                     reply_markup=InlineKeyboardMarkup().add(in_no_ad))
    await FSMTroble.description.set()


async def get_manager_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await bot.send_message(
        chat_id=CHAT,
        text=f"Пользователь {message.from_user.username}\n"
             f"Хочет связаться с менеджером.\n"
             f"Запрос:{data['description']}",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                '❗ Связаться', url=f'https://t.me/{message.from_user.username}')))
    await bot.send_message(message.from_user.id,
                           'Я передал всё менеджеру, в скором времени с вами свяжутся',
                           reply_markup=InlineKeyboardMarkup().add(in_back_main))
    await state.finish()


async def start_register(message: types.Message):
    """Запуск регистрации и проверка пользователя"""
    if db.check_user(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text=f'Ваша скидка: {sale.sale_count(message.from_user.id)}%\n'
                                    f'{sale.info_for_next(message.from_user.id)}',
                               reply_markup=back_main_menu)
    else:
        await FSMClientRegister.name.set()
        await bot.send_message(message.from_user.id, 'Пожалуйста, укажите ваше имя',
                               reply_markup=no_add)


async def add_register_name(message: types.Message, state: FSMContext):
    """Ловим имя пользователя"""
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMClientRegister.next()
    await bot.send_message(message.from_user.id,
                           'Отлично, теперь укажите номер телефона.\n'
                           'Просто нажмите кнопку снизу',
                           reply_markup=phone_contact)


async def add_phone_register(message: types.Message, state: FSMContext):
    """Ловим телефон и id """
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
        data['id'] = message.contact.user_id
        data['count'] = 0
    await db.add_user(state)
    await bot.send_message(message.from_user.id, 'Отлично, теперь у Вас есть наша\n'
                                                 'Карта Лояльности',
                           reply_markup=back_main_menu)
    await state.finish()


# KaJIuHa
def register_message_client(dis: dp):
    """Регистрация хендлеров"""
    dis.register_callback_query_handler(have_toble,
                                        text='troble')
    dis.register_callback_query_handler(wrong_description,
                                        text='w_description',
                                        state=None)
    dis.register_message_handler(photo_wrong_description,
                                 content_types=['photo'],
                                 state=FSMTroble.photo)
    dis.register_message_handler(phone_wrong_description,
                                 content_types=types.ContentType.CONTACT,
                                 state=FSMTroble.phone)
    dis.register_callback_query_handler(troble_item,
                                        text='broken')
    dis.register_callback_query_handler(trobel_item_start,
                                        text=['broken_all', 'broken_in'],
                                        state=None)
    dis.register_message_handler(trobel_item_box,
                                 content_types=['photo'],
                                 state=FSMBroken.photo)
    dis.register_message_handler(trobel_item_photo,
                                 content_types=['photo'],
                                 state=FSMBroken.photo_2)
    dis.register_message_handler(trobel_item_phone,
                                 content_types=types.ContentType.CONTACT,
                                 state=FSMBroken.phone)
    dis.register_callback_query_handler(get_manger,
                                        text='manager',
                                        state=None)
    dis.register_message_handler(get_manager_finish,
                                 state=FSMTroble.description)
    dis.register_message_handler(start_register,
                                 commands=['card'])
    dis.register_message_handler(add_register_name,
                                 state=FSMClientRegister.name)
    dis.register_message_handler(add_phone_register,
                                 content_types=types.ContentType.CONTACT,
                                 state=FSMClientRegister.phone_number)
