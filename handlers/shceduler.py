from aiogram import Bot
from services.googlesheets import get_dict_working_shift
from datetime import datetime
from config_data.config import Config, load_config

config: Config = load_config()

async def parsing_google_sheets(bot: Bot):
    current_date = datetime.now()
    # преобразуем ее в строку
    date = current_date.strftime('%d.%m.%Y')
    dict_working_shift = get_dict_working_shift(date)
    text_send = f'Коллеги, доброе утро!\n Сегодня с 10:00 до 22:00\n'
    for post in dict_working_shift.keys():
        flag = 0
        for worker in dict_working_shift[post].keys():
            if dict_working_shift[post][worker] == 'смена':
                if flag == 0:
                    text_send += f'<b>{post}</b>:\n' \
                                 f'{worker} при возникновении вопросов не забывайте ставить тег - @{worker}\n'
                    flag = 1
                else:
                    text_send += f'{worker} при возникновении вопросов не забывайте ставить тег - @{worker}\n'

    await bot.send_message(chat_id=config.tg_bot.channel_id,
                           text=text_send,
                           parse_mode='html')
if __name__ == '__main__':
    parsing_google_sheets()
