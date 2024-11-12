from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb=ReplyKeyboardMarkup()
button = KeyboardButton(text="Расчитать")
button2 = KeyboardButton(text="Информация")
kb.add(button)
kb.add(button2)

kb=InlineKeyboardMarkup()
button = InlineKeyboardButton(text = 'Расчитать норму калорий', callback_data = 'calories')
kb.add(button)
button2 = InlineKeyboardButton(text = 'Формула расчёта', callback_data = 'formulas')
kb.add(button2)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = 'Выбери опцию')],
        [
           KeyboardButton(text = 'Рассчитать норму калорий'),
           KeyboardButton(text = 'Формулы расчёта')
        ]
    ], resize_keyboard = True
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands= ['start'])
async def starter(message):
    await message.answer(text="Привет! Я бот помогающий твоему здоровью",reply_markup = kb)

@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer(text="Выбери опцию:",reply_markup = start_menu)

#@dp.callback_query_handler(text=['calories'])
#async def infor(call):
    #await call.message.answer(text="Рассчитать норму калорий")

#dp.callback_query_handler(text =['formulas'])
#async def infor(call):
    #await call.message.answer("Формулы расчёта")



@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer("10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(г) - 161")

@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()
@dp.message_handler(state = UserState.age)
async def set_growth(message,state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()
@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message,state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_wom = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f"Ваша норма калорий {calories_wom}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)