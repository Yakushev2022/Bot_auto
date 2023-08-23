from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import filter_dict # импорт функции получения машин
from main import lst_choice_json # импорт файла со словарем выбранных машин
import My_keys as key # файл с ключами
import json


bot = Bot(key.Bot_Password, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
# Задаем начальные значения
Age_from = 2010
Age_for = 2023
Mileage = 0
# Создаем клавиатуру с кнопками колбек
def get_keyboard_year():
    buttons = [
        [types.InlineKeyboardButton(text= f"{Age_from} -1", callback_data="year_decr+from"),
        types.InlineKeyboardButton(text= f"{Age_from} +1", callback_data="year_incr+from")],
        [types.InlineKeyboardButton(text=f"{Age_for} -1", callback_data="year_decr+for"),
         types.InlineKeyboardButton(text=f"{Age_for} +1", callback_data="year_incr+for")],
        [types.InlineKeyboardButton(text="-1000", callback_data="mileage_decr"),
         types.InlineKeyboardButton(text="+5000", callback_data="mileage_incr")],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="mileage_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
# Заставка с первичными данными + кнопки колбек с начальными значениями по году и пробегу
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text='Определите диапазон поиска')
    await message.answer(f'С  {Age_from} по  {Age_for} год \n Пробег: {Mileage}',  reply_markup=get_keyboard_year())
# функция обработки кнопок колбек по году
@dp.callback_query_handler(Text(startswith="year_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    global Age_from, Age_for

    if action == "incr+from":
        Age_from += 1
        await callback.message.edit_text(f'С  {Age_from} по  {Age_for} год \n Пробег : {Mileage}', reply_markup=get_keyboard_year())
    elif action == "decr+from":
        Age_from -= 1
        await callback.message.edit_text(f'С  {Age_from} по  {Age_for} год \n Пробег : {Mileage}', reply_markup=get_keyboard_year())
    elif action == "decr+for":
        Age_for -= 1
        await callback.message.edit_text(f'С  {Age_from} по  {Age_for} год \n Пробег : {Mileage}', reply_markup=get_keyboard_year())
    elif action == "incr+for":
        Age_for += 1
        await callback.message.edit_text(f'С  {Age_from} по  {Age_for} год \n Пробег : {Mileage}', reply_markup=get_keyboard_year())

    await callback.answer()
# функция обработки кнопок колбек по пробегу и подтверждения данных
@dp.callback_query_handler(Text(startswith="mileage_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    global Mileage, Age_from, Age_for
    if action == "incr":
        Mileage += 5000
        await callback.message.edit_text(f'С  {Age_from} по  {Age_for} год \n Пробег : {Mileage}', reply_markup=get_keyboard_year())
    elif action == "decr":
        Mileage -= 1000
        await callback.message.edit_text(f'С  {Age_from} по  {Age_for} год \n Пробег : {Mileage}', reply_markup=get_keyboard_year())
    elif action == "finish":
        await callback.message.answer(f'Параметры поиска: с  {Age_from} года по  {Age_for} год,  с пробегом не более: {Mileage} км.\nПожалуйста ожидайте...')
        # запускаем обрабоку запроса в теле main через функцию filter_dict()
        filter_dict(Age_from, Age_for, Mileage)

        # формируем вывод данных в ТГ из lst_choice_json
        for item in lst_choice_json:
            card = f"{hlink(item.get('URL'), item.get('Liter'))}\n" \
                   f"{hbold('Год: ')} {item.get('Год')}\n" \
                   f"{hbold('Пробег: ')} {item.get('Пробег')}\n" \
                   f"{hbold('Цена: ')} {item.get('Цена')}\n" \
                   f"{hbold('Скидочная цена: ')} {item.get('Скидочная цена')}\n"
            await callback.message.answer(card)
    await callback.answer()


executor.start_polling(dp, skip_updates=True)