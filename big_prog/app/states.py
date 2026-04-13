from aiogram.fsm.state import State, StatesGroup

class Reg(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()

class Course(StatesGroup):
    id = State()
    title = State()
    description = State()
    category = State()
    price = State()