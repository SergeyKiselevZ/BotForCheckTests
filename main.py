import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import handler_hi, handler_processing_new_test
import sys

# Запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token="")
    dp = Dispatcher()

    dp.include_routers(handler_hi.router, handler_processing_new_test.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
