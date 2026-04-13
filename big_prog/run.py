import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router
from app.db_reg import init_db

async def startup(dispatcher: Dispatcher):
    await init_db()
    print("База данных инициализирована")

async def shutdown(dispatcher: Dispatcher):
    print("Бот остановлен")

async def main():
    load_dotenv()
    bot = Bot(token='TOKEN')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('')
        print('')
        print('БОТ ВЫКЛЮЧЕН')
        print('БОТ ВЫКЛЮЧЕН')
        print('БОТ ВЫКЛЮЧЕН')
        print('')
        print('')

# "f:\PyCharm 2025.1.1.1\бот\big_prog\.venv\Scripts\Activate.ps1" для входа
# cd "F:\PyCharm 2025.1.1.1\бот\big_prog" для входа
# python run.py запуск
