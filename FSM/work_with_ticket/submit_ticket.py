from aiogram.fsm.state import StatesGroup, State


class Ticket(StatesGroup):
    set_email = State()
    set_category = State()
    set_departament = State()
    set_subject = State()
    set_message = State()
    change_email = State()