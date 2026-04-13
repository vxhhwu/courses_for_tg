import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router
from app.db_reg import init_db as init_reg
from app.db_courses import init_db as init_courses
from app.db_enroll import init_db as init_enroll

async def startup(dispatcher: Dispatcher):
    await init_reg()
    await init_courses()
    await init_enroll()
    print("Базы данных инициализированы")

async def shutdown(dispatcher: Dispatcher):
    print("Бот остановлен")

async def main():
    load_dotenv()  # загружает переменные из .env (локально)
    bot = Bot(token=os.getenv('TOKEN'))  # берёт токен из переменной окружения
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот выключен")
