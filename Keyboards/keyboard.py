from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

"""Стартовая клавиатура"""
in_1 = InlineKeyboardButton('😍Хочу оставить отзыв и получить бонус',
                            callback_data='bonus')
in_2 = InlineKeyboardButton('😔 Проблема с товаром',
                            callback_data='troble')
in_3 = InlineKeyboardButton('❓ Связаться с менеджером',
                            callback_data='manager')
in_4 = InlineKeyboardButton('👉 Наш канал', url='https://t.me/wildberriesru_official')
in_choise_start = InlineKeyboardMarkup().add(
    in_1).add(in_2).add(in_3).add(in_4)
"""Кнопка отмены"""
in_no_ad = InlineKeyboardButton('❌ Отмена',
                                callback_data='no')
"""Кнопка номера телефона"""
phone = KeyboardButton('📱 Телефон',
                       request_contact=True)
phone_contact = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True).add(phone)
"""Клавиатура для выбора в подпункте: Хочу отзыв"""
in_b1 = InlineKeyboardButton('📝 Тесктовый отзыв с бонусом',
                             callback_data='50')
in_b2 = InlineKeyboardButton('📸 Фото отзыв с бонусом',
                             callback_data='75')
in_b3 = InlineKeyboardButton('💰 Я уже оставил отзыв, хочу бонус',
                             callback_data='get_bonus')
in_back_main = InlineKeyboardButton('🏠 Вернуться в главное меню',
                                    callback_data='main')
in_choise_bonus = InlineKeyboardMarkup().add(in_b1).add(in_b2).add(in_b3).add(in_back_main)
"""Клавиатура возврата в меню и подменю 'Хочу бонус'"""
in_back_bonus = InlineKeyboardButton('↩️ Вернуться в предыдущее меню',
                                     callback_data='bonus')
link_wb = InlineKeyboardButton('🍇 Wildberries',
                               url='https://www.wildberries.ru')
in_choise_back = InlineKeyboardMarkup().add(link_wb).add(in_back_bonus).add(in_back_main)
"""Клавиатура выбора в подменю 'Проблемы с товаром'"""
in_t1 = InlineKeyboardButton('🔨 Товар поврежден',
                             callback_data='broken')
in_t2 = InlineKeyboardButton('❌ Товар не соотвествует описанию',
                             callback_data='w_description')
in_troble_choise = InlineKeyboardMarkup().add(in_t1).add(in_t2).add(in_back_main)
"""Клавиатура подменю 'Товар поврежден'"""
in_t3 = InlineKeyboardButton('Коробка и товар повреждены',
                             callback_data='broken_all')
in_t4 = InlineKeyboardButton('Коробка цела, но товар поврежден',
                             callback_data='broken_in')
in_back_broken = InlineKeyboardButton('↩️ Вернуться в предыдущее меню',
                                      callback_data='troble')
in_troble_item = InlineKeyboardMarkup().add(in_t3).add(in_t4).row(
    in_back_broken, in_back_main)
"""Кнопки в меню админа"""
in_2_ad = InlineKeyboardButton('Сделать массовую рассылку',
                               callback_data='spam')
in_admin = InlineKeyboardMarkup().add(in_2_ad)

"""Кнопка отмены"""
no_ad = InlineKeyboardButton('❌ Отмена',
                                callback_data='no')
no_add = InlineKeyboardMarkup().add(no_ad)
"""Возврат в главное меню"""
back_main = InlineKeyboardButton('🏠 Вернуться в главное меню',
                                 callback_data='main')
back_main_menu = InlineKeyboardMarkup().add(
    back_main)
