from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import debug

def make_row_base_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    if debug:
        row = [KeyboardButton(text=item) for item in items]
        row.append(KeyboardButton(text='/start'))
    else:
        row = [KeyboardButton(text=item) for item in items]

    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
