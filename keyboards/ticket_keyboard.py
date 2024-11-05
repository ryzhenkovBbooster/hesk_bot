from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

category = [
    {
        "id": 1,
        "name": 'Google Workspace'
    },
{
        "id": 2,
        "name": 'Телефония'
    },
{
        "id": 3,
        "name": 'VPN'
    },
    {
        "id": 4,
        "name": 'Zoom'
    },
{
        "id": 5,
        "name": 'Getcourse'
    },
{
        "id": 6,
        "name": 'Lastpass'
    },
    {
        "id": 7,
        "name": 'Telegram'
    },
{
        "id": 8,
        "name": 'AmoCRM'
    },
{
        "id": 9,
        "name": 'Другие сервисы'
    },
# {
#         "id": 10,
#         "name": ''
#     },
{
        "id": 11,
        "name": 'Textback'
    },
{
        "id": 12,
        "name": 'BB Platform'
    },
]

departaments = [
    "I", "II", "III", "IV", "V", "VIa", "VIb", "VII"
]

def cmd_start_k() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    kb.button(text='Создать заявку')

    return kb.as_markup(resize_keyboard=True)
def create_ticket_k(email: str):
    rows = []
    # print(email, type(email))
    if "None" not in email and email is not False:
        rows.append([InlineKeyboardButton(text=email, callback_data=f'email_data {email}')])
        rows.append([InlineKeyboardButton(text="Сменить почту", callback_data='change_email')])
    rows.append([InlineKeyboardButton(text='Пропустить', callback_data='skip_email')])
    return InlineKeyboardMarkup(inline_keyboard=rows)
def set_category_k():
    rows = [[InlineKeyboardButton(text=item['name'], callback_data=str(item['id']))] for item in category]

    # Добавляем кнопку 'Отмена' в отдельный ряд
    # rows.append([InlineKeyboardButton(text='Отмена', callback_data='back_to_menu')])

    # Создаем клавиатуру без указания row_width, так как каждый ряд уже определен
    return InlineKeyboardMarkup(inline_keyboard=rows)

def set_departaments_k():
    rows = [[InlineKeyboardButton(text=item, callback_data=item)] for item in departaments]

    # Добавляем кнопку 'Отмена' в отдельный ряд
    # rows.append([InlineKeyboardButton(text='Отмена', callback_data='back_to_menu')])

    # Создаем клавиатуру без указания row_width, так как каждый ряд уже определен
    return InlineKeyboardMarkup(inline_keyboard=rows)