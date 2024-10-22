import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import API_TOKEN
from bot.handlers import admin, user
from bot.models.database import create_db_and_tables

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(user.router)
    dp.include_router(admin.router)

    await set_commands(bot)
    await create_db_and_tables()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Start the bot."),
        BotCommand(command="/settings", description="Settings of the bot."),
        BotCommand(command="/admin", description="Admin panel."),
    ]
    await bot.set_my_commands(commands)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
