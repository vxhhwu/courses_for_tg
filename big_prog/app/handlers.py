from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.enums import ChatAction
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.states import Reg, Course
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.kb as kb

from app.db_reg import save_user, get_user, del_user, user_exists

from app.db_courses import save_new_course, get_courses, get_courses_by_category, del_courses, get_course_by_id

from app.db_enroll import add_my_course, get_my_courses, is_already_enrolled, del_my_course

router = Router()

CATEGORY_NAMES = {
    'biology': 'Биология',
    'maths': 'Математика',
    'russian': 'Русский язык',
    'chemistry': 'Химия',
    'programming': 'Программирование'
}

@router.message(Command('reg'))
async def cmd_reg(message: Message, state: FSMContext):
    if await user_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы")
        return
    await state.set_state(Reg.first_name)
    await message.answer('Отправьте своё имя')
    
@router.message(Reg.first_name)
async def cmd_reg_first_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение с именем\n/reg Для регистрации")
        return
    await state.update_data(first_name=message.text)
    await state.set_state(Reg.last_name)
    await message.answer('Отправьте вашу фамилию')

@router.message(Reg.last_name)
async def cmd_reg_last_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение с фамилией\n/reg Для регистрации")
        return
    await state.update_data(last_name=message.text)
    await state.set_state(Reg.age)
    await message.answer('Отправьте ваш возраст(только число!)')

@router.message(Reg.age)
async def cmd_reg_age(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение с возрастом\n/reg Для регистрации")
        return
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Возраст должен быть числом. Попробуйте ещё раз.")
        return
    await state.update_data(age=age)
    data = await state.get_data()

    # <-- NEW: сохраняем данные в БД
    await save_user(
        user_id=message.from_user.id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=age
    )
    kb_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='В Меню', callback_data='back_to_main')]
    ])
    await message.answer(f'Ваш профиль:\nИмя: {data["first_name"]}\nФамилия: {data["last_name"]}\nВозраст: {data["age"]}', reply_markup=kb_menu)
    await state.clear()

@router.message(Command('adm_dc'))
async def cmd_delete_course(message: Message):
    if message.from_user.id == 1385387997:
        parts = message.text.split()
        id = int(parts[1])
        deleted = await del_courses(id)
        if deleted:
            await message.answer(f"✅ Курс с ID {id} успешно удалён.")
            return
        else:
            await message.answer(f"❌ Курс с ID {id} не найден.")
            return
    await message.answer('Извиняюсь, но вы не администратор')

@router.message(Command('adm_gc'))
async def cmd_get_courses(message: Message):
    if message.from_user.id == 1385387997:
        courses = await get_courses()
        if not courses:
            await message.answer('Саксэс, ты пока не добавлял курсов')
            return
        text = "Список курсов:\n"
        for course in courses:
            text += f"{course[1]}. {course[2]} - {course[4]} руб.\n"
        await message.answer(text)
        return
    await message.answer('Извиняюсь, но вы не администратор')

@router.message(Command('adm_sc'))
async def cmd_add_courses_by_adm(message: Message, state: FSMContext):
    if message.from_user.id == 1385387997:
        await state.set_state(Course.id)
        await message.reply('Привет Саксэс!\nНапиши ID курса')
        return
    await message.answer('Извиняюсь, но вы не администратор')

@router.message(Course.id)
async def cmd_set_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await state.set_state(Course.title)
    await message.answer('Введи название курса')

@router.message(Course.title)
async def cmd_set_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Course.description)
    await message.answer('Введи описание курса')

@router.message(Course.description)
async def cmd_set_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Course.category)
    await message.answer('Введи категорию курса')
    await message.answer('Примеры категорий(для будущего): biology, maths, russian, chemistry, program')

@router.message(Course.category)
async def cmd_set_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(Course.price)
    await message.answer('Введи цену за курс')

@router.message(Course.price)
async def cmd_set_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer('Готово Саксэс! /adm_gc для выведения курсов')
    data = await state.get_data()
    await save_new_course(
        id = data['id'],
        title = data['title'],
        description = data['description'],
        category = data['category'],
        price = data['price']
    )
    await state.clear()

@router.callback_query(F.data == 'back_to_main')
async def cmd_back_to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Меню', reply_markup=kb.inline_main)

@router.callback_query(F.data == 'catalog')
async def cmd_catalog(callback: CallbackQuery):
    if await user_exists(callback.from_user.id):
        await callback.answer('Вы выбрали Каталог')
        await callback.message.edit_text('Выберите тему', reply_markup=kb.catalog_inline)
        return
    await callback.message.edit_text('Вы не зарегистрированы\n /reg Для регистрации')

@router.callback_query(F.data == 'contacts')
async def cmd_contacts(callback: CallbackQuery):
    await callback.answer('Вы выбрали Контакты')
    await callback.message.edit_text('Контакты', reply_markup=kb.contacts_inline)

@router.callback_query(F.data == 'lk')
async def cmd_lk(callback: CallbackQuery):
    await callback.answer('Вы выбрали Личный Кабинет')
    user_data = await get_user(callback.from_user.id)
    if user_data:
        text = (f"Личный кабинет:\n"
                f"ID: {callback.from_user.id}\n"
                f"Имя: {user_data['first_name']}\n"
                f"Фамилия: {user_data['last_name']}\n"
                f"Возраст: {user_data['age']}")
    else:
        text = f"Личный кабинет:\nВаш ID: {callback.from_user.id}\nВы не зарегистрированы. Используйте /reg"
    lk_keybord = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мои курсы', callback_data='my_courses')],
        [InlineKeyboardButton(text='Удалить профиль', callback_data='del_self_profile')],
        [InlineKeyboardButton(text='Назад в меню', callback_data='back_to_main')]
    ])
    await callback.message.edit_text(text, reply_markup=lk_keybord)

@router.callback_query(F.data == 'del_self_profile')
async def cmd_sure_to_delete(callback: CallbackQuery):
    text = 'Вы уверены что хотите удалить свой профиль?'
    del_user_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да, уверен', callback_data='sure_to_del')],
        [InlineKeyboardButton(text='Нет, передумал', callback_data='lk')]
    ])
    await callback.message.edit_text(text, reply_markup=del_user_kb)

@router.callback_query(F.data == 'sure_to_del')
async def cmd_delete_user(callback: CallbackQuery):
    await callback.message.edit_text('Удаляю ваш профиль')
    await asyncio.sleep(0.5)
    del_user_from_db = await del_user(callback.from_user.id)
    text = 'Профиль успешно удален'
    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад в меню', callback_data='back_to_main')]
    ])
    await callback.message.edit_text(text, reply_markup=back_kb)

@router.callback_query(F.data == 'my_courses')
async def cmd_show_my_courses(callback: CallbackQuery):
    user_id = callback.from_user.id
    courses = await get_my_courses(user_id)
    if not courses:
        back_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="lk")]
        ])
        await callback.message.edit_text("📭 У вас пока нет записанных курсов.", reply_markup=back_kb)
        return

    text = "📚 <b>Ваши курсы:</b>\n\n"   # или оставьте просто заголовок
    keyboard_buttons = []
    for course_id, title, description, category, price in courses:
        # Преобразуем английскую категорию в русскую
        category_ru = CATEGORY_NAMES.get(category, category)  # если нет в словаре, оставляем как есть
        button_text = f"📖 {title} ({category_ru})"
        keyboard_buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"mycourse_{course_id}")])
    keyboard_buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="catalog")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith('mycourse_'))
async def cmd_info_my_course(callback: CallbackQuery):
    course_id = int(callback.data.split('_')[1])

    one_course = await get_course_by_id(course_id)

    if not one_course:
        await callback.answer("Курс не найден", show_alert=True)
        await callback.message.edit_text("Извините, этот курс больше недоступен.")
        return

    title, description, category, price = one_course
    inline_courseid_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отписаться от курса',callback_data=f'del_my_course_{course_id}')],
        [InlineKeyboardButton(text='В Личный кабинет', callback_data='lk')]
    ])
    await callback.message.edit_text(f'Название курса:{title}\n\nОписание курса:{description}\nЦена:{price}', reply_markup=inline_courseid_kb)
    await callback.answer()

@router.callback_query(F.data.startswith('del_my_course_'))
async def cmd_del_my_course(callback: CallbackQuery):
    course_id = int(callback.data.split('_')[3])
    user_id = int(callback.from_user.id)

    del_course = await del_my_course(user_id, course_id)
    if del_course:
        await callback.answer("Курс удалён из вашего списка", show_alert=False)
        await callback.message.edit_text("✅ Курс удалён из ваших курсов.")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="В Мои курсы", callback_data="my_courses")]
        ])
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    else:
        await callback.answer("Не удалось удалить курс или он уже удалён", show_alert=True)

@router.callback_query(F.data.startswith('category_'))
async def cmd_show_courses_by_category(callback: CallbackQuery):
    # с помощью сплита разделяем названрие колбэка и через [1] получаем название курса
    category_en = callback.data.split('_', 1)[1]
    category_ru = CATEGORY_NAMES.get(category_en)
    
    courses = await get_courses_by_category(category_en)
    
    if not courses:
        await callback.answer("В этой категории пока нет курсов")
        back_btn = InlineKeyboardButton(text="🔙 Назад", callback_data="catalog")
        await callback.message.edit_text(
            "Курсы не найдены.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[back_btn]])
        )
        return
    
    # делаем список и строим из него инлайн кнопки
    keyboard_buttons = []
    for course in courses:
        id, title = course
        # при нажатии на курс выводим колбэк дату с айди курса
        keyboard_buttons.append([
            InlineKeyboardButton(text=title, callback_data=f"course_{id}")
        ])
    
    # в конце добавляем кнопку назад в каталог
    keyboard_buttons.append([
        InlineKeyboardButton(text="🔙 Назад к категориям", callback_data="catalog")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(f"📚 Курсы в категории «{category_ru}»:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith('course_'))
async def cmd_show_course_by_id(callback: CallbackQuery):
    course_id = int(callback.data.split('_', 1)[1])

    one_course = await get_course_by_id(course_id)

    if not one_course:
        await callback.answer("Курс не найден", show_alert=True)
        await callback.message.edit_text("Извините, этот курс больше недоступен.")
        return

    title, description, category, price = one_course
    inline_courseid_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Записаться на курс', callback_data=f'enroll_{course_id}')],
        [InlineKeyboardButton(text='Назад в каталог курсов', callback_data='catalog')]
    ])
    await callback.message.edit_text(f'Название курса:{title}\n\nОписание курса:{description}\nЦена:{price}', reply_markup=inline_courseid_kb)
    await callback.answer()

@router.callback_query(F.data.startswith('enroll_'))
async def cmd_add_my_course(callback: CallbackQuery):
    course_id = int(callback.data.split('_')[1])
    user_id = callback.from_user.id

    # существует ли курс в общем каталоге
    course = await get_course_by_id(course_id)
    if not course:
        await callback.answer("Курс не найден", show_alert=True)
        await callback.message.edit_text("❌ Извините, этот курс больше недоступен.")
        return

    # не записан ли уже пользователь на курс
    if await is_already_enrolled(user_id, course_id):
        await callback.answer("Вы уже записаны на этот курс!", show_alert=True)
        return

    # распаковка данных курса
    title, description, category, price = course

    success = await add_my_course(user_id, course_id, title, description, category, price)
    if success:
        back_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='В каталог', callback_data='catalog')]
        ])
        await callback.answer("✅ Вы успешно записаны на курс!", show_alert=False)
        # Можно изменить сообщение, чтобы показать подтверждение
        await callback.message.edit_text(f"{title}\n\nВы записаны на этот курс!", reply_markup=back_kb)
    else:
        await callback.answer("Не удалось записаться. Попробуйте позже.", show_alert=True)

@router.message(CommandStart)
async def cmd_hi(message: Message):
    await message.reply(f'Привет, {message.from_user.first_name}!\nЯ - бот для подбора курса по твоему запросу\n/reg Для регистрации')
    await message.answer('Меню', reply_markup = kb.inline_main)

@router.message()
async def cmd_empty_message(message: Message):
    await message.reply('Введи /start для запуска меню')
