from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from print_color import print
#import db
import os
import pathlib
import shutil
from keyboard import make_row_base_keyboard
#from photo_processing2 import photoProcessing

import processing_test
import config

router = Router()

class States(StatesGroup):
    cl = State()
    name = State()
    answers = State()
    criteria = State()
    photo = State()

#@router.message(default_state, F.text == "Проверить тест")
async def new_test(message: Message, state: FSMContext):
    if config.debug:
        await message.answer(
            text="Пришлите фото работ. Фото должно быть качественным, освещение равномерным.\
                На одном фото может быть несколько работ, но между ними должно быть небольшое расстояние.\
                Как только вы завершите нажмите кнопку 'Это всё' на моей клавиатуре",
            reply_markup=make_row_base_keyboard(['Это всё', 'Назад'])
        )

        await state.set_state(States.photo)
    else:
        await message.answer(
            text="Введите класс",
            reply_markup=make_row_base_keyboard(['Назад'])
        )

        await state.set_state(States.cl)


#@router.message(States.cl, F.text == 'Назад')
@router.message(States.answers, F.text == 'Назад')
async def choose_cl_back(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вернулись в главное меню",
        reply_markup=make_row_base_keyboard(['Проверить тест'])
    )

    await state.set_state(default_state)

@router.message(States.cl, F.text)
async def choose_cl(message: Message, state: FSMContext):
    await state.update_data(cl=message.text.upper())
    await message.answer(
        text="Хорошо, теперь введите название теста",
        reply_markup=make_row_base_keyboard(['Назад'])
    )

    await state.set_state(States.name)

@router.message(States.name, F.text == 'Назад')
async def choose_name_back(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вернулись назад. Пожалуйста введите повторно класс",
        reply_markup=make_row_base_keyboard(['Назад'])
    )

    await state.set_state(States.cl)

@router.message(default_state, F.text == "Проверить тест")
#@router.message(States.name, F.text)
async def choose_name(message: Message, state: FSMContext):
    #await state.update_data(name=message.text.capitalize())
    await message.answer(
        text="Введите правильные ответы: сначала номер задания потом ответ через пробел, каждый ответ запишите в новой строке:\n1 2\n2 4\n3 1\n...",
        reply_markup=make_row_base_keyboard(['Назад'])
    )

    await state.set_state(States.answers)

#@router.message(States.answers, F.text == 'Назад')
@router.message(default_state, F.text == 'Назад')
async def choose_answers_back(message: Message, state: FSMContext):
    await message.answer(
        #text="Вы вернулись назад. Пожалуйста введите повторно название теста",
        #reply_markup=make_row_base_keyboard(['Назад'])
        text="Здравствуйте:) Я бот, который помогает учителям проверять тесты, написанные от руки. Нажмите на кнопку на моей клавиатуре ",
        reply_markup=make_row_base_keyboard(['Проверить тест'])
    )

    #await state.set_state(States.name)



@router.message(States.answers, F.text)
async def choose_answers(message: Message, state: FSMContext):
    await state.update_data(answers=message.text.lower())
    await message.answer(
        text="Введите критерии оценивания. Напишите оценку, через пробел напишите минимальное количество баллов, которое нужно получить для этой оценки:\n5 10\n4 8\n3 6\n2 4",
        reply_markup=make_row_base_keyboard(['Назад'])
    )

    await state.set_state(States.criteria)

@router.message(States.criteria, F.text == 'Назад')
async def choose_criteria_back(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вернулись назад. Пожалуйста введите повторно правильные ответы",
        reply_markup=make_row_base_keyboard(['Назад'])
    )

    await state.set_state(States.answers)

@router.message(States.criteria, F.text)
async def choose_criteria(message: Message, state: FSMContext):
    await state.update_data(criteria=message.text.lower())
    await message.answer(
        text="Пришлите фото работ. Фото должно быть качественным, освещение равномерным. На одном фото может быть несколько работ, но между ними должно быть небольшое расстояние. Как только вы завершите нажмите кнопку 'Это всё' на моей клавиатуре",
        reply_markup=make_row_base_keyboard(['Это всё', 'Назад'])
    )

    await state.set_state(States.photo)
    user_id = message.from_user.id
    if os.path.exists(f'tmp/{user_id}'):
        shutil.rmtree(f'tmp/{user_id}')
    os.mkdir(f'tmp/{user_id}')

@router.message(States.photo, F.text == 'Назад')
async def get_photo_back(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вернулись назад. Пожалуйста введите повторно критерии оценивания",
        reply_markup=make_row_base_keyboard(['Назад'])
    )

    await state.set_state(States.criteria)

@router.message(States.photo, F.text == 'Повторить попытку')
async def end_get_photo(message: Message, state: FSMContext):
    await message.answer(
        text="Повторная обработка, пожалуйста, подождите",
        reply_markup=ReplyKeyboardRemove()
    )
    user_data = await state.get_data()
    user_id = message.from_user.id
    user_data['user_id'] = user_id
    path = f'tmp/{user_id}/'

    if os.path.exists(f'tests/{user_id}'):
        shutil.rmtree(f'tests/{user_id}')
    os.mkdir(f'tests/{user_id}')

    try:
        res = await processing_test.main_processing(user_id,user_data)
    except Exception as error:
        await message.answer(
            text='Упс:(\nЧто-то пошло не так. Повторите попытку, нажав кнопку на моей клавиатуре',
            reply_markup=make_row_base_keyboard(['Повторить попытку', 'В главное меню'])
        )

        shutil.rmtree(f'tests/{user_id}')
        print(error, tag='Error', tag_color='red', color='magenta')
    else:
        await message.answer(
            text=res,
            reply_markup=make_row_base_keyboard(['Проверить тест'])
        )
        await state.set_state(default_state)

        shutil.rmtree(path)
        shutil.rmtree(f'tests/{user_id}')


@router.message(States.photo, F.text == 'В главное меню')
async def to_main_menu(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(
        # text="Вы вернулись назад. Пожалуйста введите повторно название теста",
        # reply_markup=make_row_base_keyboard(['Назад'])
        text="Здравствуйте:) Я бот, который помогает учителям проверять тесты, написанные от руки. Нажмите на кнопку на моей клавиатуре ",
        reply_markup=make_row_base_keyboard(['Проверить тест'])
    )
    user_id = message.from_user.id
    shutil.rmtree(f'tmp/{user_id}')


@router.message(States.photo, F.text == 'Это всё')
async def end_get_photo(message: Message, state: FSMContext):
    await message.answer(
        text="Идёт обработка, пожалуйста, подождите",
        reply_markup=ReplyKeyboardRemove()
    )
    user_data = await state.get_data()
    user_id = message.from_user.id
    user_data['user_id'] = user_id
    path = f'tmp/{user_id}/'

    if os.path.exists(f'tests/{user_id}'):
        shutil.rmtree(f'tests/{user_id}')
    os.mkdir(f'tests/{user_id}')

    try:
        res = await processing_test.main_processing(user_id,user_data)
    except Exception as error:
        await message.answer(
            text='Упс:(\nЧто-то пошло не так. Повторите попытку, нажав кнопку на моей клавиатуре',
            reply_markup=make_row_base_keyboard(['Повторить попытку', 'В главное меню'])
        )

        shutil.rmtree(f'tests/{user_id}')
        print(error, tag='Error', tag_color='red', color='magenta')
    else:
        await message.answer(
            text=res,
            reply_markup=make_row_base_keyboard(['Проверить тест'])
        )
        await state.set_state(default_state)

        shutil.rmtree(path)
        shutil.rmtree(f'tests/{user_id}')


@router.message(States.photo, F.photo)
async def get_photo(message: Message, bot: Bot):
    path = f'tmp/{message.from_user.id}'
    if not os.path.isdir(path):
        os.mkdir(path)

    try:
        await bot.download(
            message.photo[-1],
            destination=path+'/'+str(message.photo[-1].file_id)+'.jpg'
        )
    except:
        await message.answer(
            text="Упс:(\nПовторите отправку фото",
        )