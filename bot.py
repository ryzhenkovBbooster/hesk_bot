import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

from db.database import db_init, sessionmaker
from handlers import send_ticket
from middlewarews.db import DbSessionMiddleware
from middlewarews.register_check import RegisterCheck

load_dotenv()
dp = Dispatcher()

TOKEN = os.getenv("TOKEN")

async def on_startup():
    await db_init()
async def main() -> None:
    dp.startup.register(on_startup)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.message.middleware(RegisterCheck(session_pool=sessionmaker))

    dp.include_router(send_ticket .router)

    # dp.include_routers(access.router, chat.router, check_messages.router)
    bot = Bot(TOKEN)

    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())