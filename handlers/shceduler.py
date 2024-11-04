from aiogram import Bot
from services.googlesheets import get_dict_working_shift
from datetime import datetime
from config_data.config import Config, load_config

config: Config = load_config()


async def parsing_google_sheets_day(bot: Bot):
    current_date = datetime.now()
    # преобразуем ее в строку
    date = current_date.strftime('%d.%m.%Y')
    dict_working_shift = get_dict_working_shift(date)
    text_send_1 = f'Коллеги, доброе утро!\n Сегодня с 10:00 до 22:00\n'
    text_send_2 = ''
    for post in dict_working_shift.keys():
        flag = 0
        if "Менеджеры парка" not in post:
            for worker in dict_working_shift[post].keys():
                if dict_working_shift[post][worker] == 'день':
                    if flag == 0:
                        text_send_1 += f'<b>{post}</b>:\n' \
                                     f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'
                        flag = 1
                    else:
                        text_send_1 += f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'
        else:
            for worker in dict_working_shift[post].keys():
                if dict_working_shift[post][worker] == 'день':
                    if flag == 0:
                        text_send_2 += f'<b>{post}</b>:\n' \
                                       f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'
                        flag = 1
                    else:
                        text_send_2 += f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'

    await bot.send_message(chat_id=config.tg_bot.channel_id,
                           text=text_send_1,
                           parse_mode='html')
    if text_send_2 != '':
        await bot.send_message(chat_id=config.tg_bot.channel_id,
                               text=text_send_2,
                               parse_mode='html')


async def parsing_google_sheets_night(bot: Bot):
    current_date = datetime.now()
    # преобразуем ее в строку
    date = current_date.strftime('%d.%m.%Y')
    dict_working_shift = get_dict_working_shift(date)
    text_send_1 = f'Коллеги, доброе утро!\n Сегодня с 22:00 до 10:00\n'
    text_send_2 = ''
    for post in dict_working_shift.keys():
        flag = 0
        if "Менеджеры парка" not in post:
            for worker in dict_working_shift[post].keys():
                if dict_working_shift[post][worker] == 'ночь':
                    if flag == 0:
                        text_send_1 += f'<b>{post}</b>:\n' \
                                       f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'
                        flag = 1
                    else:
                        text_send_1 += f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'
        else:
            for worker in dict_working_shift[post].keys():
                if dict_working_shift[post][worker] == 'ночь':
                    if flag == 0:
                        text_send_2 += f'<b>{post}</b>:\n' \
                                       f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'
                        flag = 1
                    else:
                        text_send_2 += f'{worker.split("@")[0]} при возникновении вопросов не забывайте ставить тег - @{worker.split("@")[1]}\n'

    await bot.send_message(chat_id=config.tg_bot.channel_id,
                           text=text_send_1,
                           parse_mode='html')
    if text_send_2 != '':
        await bot.send_message(chat_id=config.tg_bot.channel_id,
                               text=text_send_2,
                               parse_mode='html')

if __name__ == '__main__':
    pass