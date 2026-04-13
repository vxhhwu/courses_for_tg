from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Каталог', callback_data='catalog'),
    InlineKeyboardButton(text = 'Контакты', callback_data='contacts')], # доделано
    [InlineKeyboardButton(text = 'Личный кабинет', callback_data='lk')] # доделано
])

catalog_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Биология', callback_data='category_biology'),
    InlineKeyboardButton(text = 'Математика', callback_data='category_maths')],
    [InlineKeyboardButton(text = 'Русский яз.', callback_data='category_russian'),
    InlineKeyboardButton(text = 'Химия', callback_data='category_chemistry')],
    [InlineKeyboardButton(text = 'Программирование', callback_data='category_programming')],
    [InlineKeyboardButton(text = 'Назад в меню', callback_data='back_to_main')]
])

contacts_inline = InlineKeyboardMarkup(inline_keyboard=[ # доделано
    [InlineKeyboardButton(text = 'Почта', url='tai.amanzh@vk.com'),
    InlineKeyboardButton(text = 'Сотовый', url=('+79869130510'))],
    [InlineKeyboardButton(text = 'Личный чат', url='https://t.me/ne6esnblyplugg')],
    [InlineKeyboardButton(text = 'Назад в меню', callback_data='back_to_main')]
])