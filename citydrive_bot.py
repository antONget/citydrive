import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.shceduler import parsing_google_sheets_day, parsing_google_sheets_night
from aiogram.types import ErrorEvent, FSInputFile
import traceback
from handlers import other_handlers
# Инициализируем logger
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # create_table_users()
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    dp.include_router(other_handlers.router)
    # каждый день
    scheduler.add_job(parsing_google_sheets_day, 'cron', hour=9, minute=50, args=(bot,))
    scheduler.add_job(parsing_google_sheets_night, 'cron', hour=21, minute=50, args=(bot,))
    scheduler.start()

    # @dp.error()
    # async def error_handler(event: ErrorEvent):
    #     logger.critical("Критическая ошибка: %s", event.exception, exc_info=True)
    #     await bot.send_message(chat_id=843554518,
    #                            text=f'{event.exception}')
    #     formatted_lines = traceback.format_exc()
    #     text_file = open('error.txt', 'w')
    #     text_file.write(str(formatted_lines))
    #     text_file.close()
    #     await bot.send_document(chat_id=843554518,
    #                             document=FSInputFile('error.txt'))
    # Пропускаем накопившиеся update и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
