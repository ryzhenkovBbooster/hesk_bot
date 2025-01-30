import requests
import os
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from FSM.work_with_ticket.submit_ticket import Ticket
from keyboards.ticket_keyboard import create_ticket_k, cmd_start_k, set_category_k, set_departaments_k
from service.submit_ticket_service import get_email_to_user, update_email_to_user

router = Router()

load_dotenv()

HESK_USERNAME = os.getenv("HESK_USERNAME")
HESK_PASSWORD = os.getenv("HESK_PASSWORD")

@router.message(Command('start', prefix='!/') )
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    if message.chat.type == 'private':

        await message.answer(
            "Привет!",
            reply_markup=cmd_start_k()
        )



# @router.callback_query(Add_access.get_user, F.data == 'cancel')
# @router.callback_query(Add_access.edit_access, F.data == 'cancel')
# async def back_to_menu_inline(callback: CallbackQuery, state: FSMContext):
#         await state.clear()
#         await callback.message.answer('back to menu', reply_markup=crud_premission())

@router.message(F.text.lower() == "создать заявку")
async def create_ticket(message: Message, state: FSMContext, session: AsyncSession):
    await state.set_state(Ticket.set_email)
    email = await get_email_to_user(user_id=int(message.from_user.id), session=session)


    await message.answer('Введите адрес эл. почты (необязательно)', reply_markup=create_ticket_k(email))

@router.callback_query(F.data == 'change_email')
async def change_email(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(Ticket.change_email)
    await callback.message.answer('Введите новый адрес эл. почты')
@router.message(Ticket.change_email)
async def finaly_change_email(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    email = message.text
    if '@'  in email:
        await update_email_to_user(user_id=message.from_user.id, session=session, email=email)
    await message.answer('Почта изменена', reply_markup=cmd_start_k())



@router.callback_query(Ticket.set_email)
async def set_category_callback(callback: CallbackQuery, state: FSMContext):
    if 'email_data' in callback.data:
        email = callback.data.split(' ')[1]
        await state.update_data(email=email)

        await state.set_state(Ticket.set_category)
        await callback.message.answer(f'Укажите категорию', reply_markup=set_category_k())
    else:
        email = 'admin@bbooster.online'
        await state.update_data(email=email)
        await state.set_state(Ticket.set_category)
        await callback.message.answer('Укажите категорию', reply_markup=set_category_k())

@router.message(Ticket.set_email)
async def set_category_message(message: Message, state: FSMContext, session: AsyncSession):


    email = message.text if hasattr(message, 'text') else "None"

    # call_answer = None

    if '@' not in email:
        email = 'admin@bbooster.online'
    else:
        await update_email_to_user(user_id=message.from_user.id, session=session, email=email)
    await state.update_data(email=email)
    await state.set_state(Ticket.set_category)
    await message.answer("Укажите категорию", reply_markup=set_category_k())

@router.callback_query(Ticket.set_category)
async def set_departament(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await state.set_state(Ticket.set_subject)

    await callback.message.answer("Тема запроса")


# @router.callback_query(Ticket.set_departament)
# async def set_subject(callback: CallbackQuery, state: FSMContext):
#     await state.update_data(departament=callback.data)
#     await state.set_state(Ticket.set_subject)
#     await callback.message.answer("Тема запроса")


@router.message(Ticket.set_subject)
async def set_message(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(Ticket.set_message)
    await message.answer("Опишите задачу")

@router.message(Ticket.set_message)
async def submit_ticket(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    data = await state.get_data()
    send_to_hesk(data, message)
    await message.answer("Заявка отправлена")




def send_to_hesk(state_data: dict, message):

    url = 'https://support.visotsky.com/admin/admin_submit_ticket.php'
    session = requests.Session()

    url_auth = 'https://support.visotsky.com/admin/index.php'
    headers = {
        # "Content-Type": "text/html; charset=utf-8",
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    data = {
        "user": HESK_USERNAME,
        "pass": HESK_PASSWORD,
        'remember_user': 'NOTHANKS',
        "a": "do_login"
    }

    response = session.post(url_auth, data=data, headers=headers)
    token = response.text.split('token=')[1].split('">')[0]
    data_response = {
        "change_category": 0,
        "saved_replies": 0,
        'notify': 1,
        'show': 0,
        "owner": '-1',
        "category": state_data['category'],
        "status": 0,
        # "custom1": state_data['departament'],
        "mode": 1,
        "subject": state_data['subject'],
        "message": state_data['message'],
        "name": message.from_user.full_name,
        "email": state_data['email'],
        "priority": 3,
        "as_language": "Pусский",
        "token": token
    }
    session.post(url, headers=headers, data=data_response)

    session.close()
# testresp()