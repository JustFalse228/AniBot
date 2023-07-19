from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram import types
from AnimeTitles.db import get_title_id

button_find = "🔎 Найти аниме"
button_random = "🎲 Случайный Тайтл"
button_report = "💬 Баг-репорт"
button_profile = "👤 Профиль"

mainMarkup = (
    ReplyKeyboardMarkup(resize_keyboard=True).row(button_find, button_random, button_report).row(button_profile)
)


def inlineView(nameTitle, userId):
    inline_viewed = "👀 Добавить в просмотренные"
    inline_view = "🔭 Смотрю сейчас"

    title_id = get_title_id(nameTitle)

    inlineButton = types.InlineKeyboardMarkup(row_width=1)
    inlineBtnViewed = types.InlineKeyboardButton(inline_viewed, callback_data=f"ud_{title_id}_{userId}_1")
    inlineBtnView = types.InlineKeyboardButton(inline_view, callback_data=f"uw_{title_id}_{userId}")

    inlineButton.add(inlineBtnViewed, inlineBtnView)

    return inlineButton

def profileBtn():
    check_titles = "👀 Мой список Аниме"
    inlineProfile = types.InlineKeyboardMarkup(row_width=1)
    inlineProfileAdd = types.InlineKeyboardButton(check_titles, callback_data="profile_titles")

    inlineProfile.add(inlineProfileAdd)

    return inlineProfile

def removeToView(id, titleId):
    removeBtn = "🗑 Убрать из просмотренных"
    removeMarkup = types.InlineKeyboardMarkup(row_width=1)
    removeButton = types.InlineKeyboardButton(removeBtn, callback_data=f"rmve_{titleId}_{id}_1")

    removeMarkup.add(removeButton)

    return removeMarkup

def views_title(userId, title_id):
    btn1 = "➕ Добавить в Просмотренные"
    btn2 = "➖ Убрать из Просматриваемых"

    btnsMarkup = types.InlineKeyboardMarkup(row_width=1)
    btns1 = types.InlineKeyboardButton(btn1, callback_data=f"ud_{title_id}_{userId}_2")
    btns2 = types.InlineKeyboardButton(btn2, callback_data=f"rmve_{title_id}_{userId}_2")

    btnsMarkup.add(btns1, btns2)

    return btnsMarkup

def backToProfile():
    btnText = "⬅️ Назад в Профиль"
    
    btnMarkup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(btnText, callback_data=f"back_to_profile")
    btnMarkup.add(btn)

    return btnMarkup