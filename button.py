from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, callback_query

mid = InlineKeyboardButton('Мой ID', callback_data='mid')
yid = InlineKeyboardMarkup().add(mid)

unban = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Вернуть', callback_data='unban'))
unmute = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Размутить', callback_data='unmute'))