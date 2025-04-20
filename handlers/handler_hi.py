from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboard import make_row_base_keyboard

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Здравствуйте:) Я бот, который помогает учителям проверять тесты, написанные от руки. Нажмите на кнопку на моей клавиатуре ",
        reply_markup=make_row_base_keyboard(['Проверить тест'])
    )
