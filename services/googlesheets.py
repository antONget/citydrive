import gspread
import logging


# gp = gspread.service_account(filename='services/keys.json')
gp = gspread.service_account(filename='keys.json')
gsheet = gp.open('График для бота')
sheet = gsheet.worksheet("Лист1")


def get_dict_working_shift(date: str) -> dict:
    """
    Получаем список пользователей работающих в заданный день date
    :param date: дата в формате хх.хх.хххх
    :return: dict
    """
    logging.info(f'get_list_working_shift')
    values = sheet.get_all_values()
    first_row = values[0]
    index_date = first_row.index(date)
    dict_working_shift = {}
    for i, row in enumerate(values[1:]):
        if row[0] != '':
            post = row[0]
            dict_working_shift[post] = {}
        if row[1] != '':
            dict_working_shift[post][row[1]] = row[index_date]
    return dict_working_shift


# def get_list_orders():
#     logging.info(f'get_list_orders')
#     values = order_sheet.get_all_values()
#     list_orders = []
#     for item in values:
#         list_orders.append(item)
#     return list_orders
#
#
# def get_key_product(category: str, product: int) -> list:
#     logging.info(f'get_key_product')
#     # print("product:", product)
#     sheet = dict_category[category]
#     values = sheet.get_all_values()
#     list_key = []
#     for i, item in enumerate(values):
#         # print(item[product:product+7])
#         slice_item = item[product*7:product*7+7]
#         slice_item.append(i)
#         list_key.append(slice_item)
#     return list_key
#
#
# def get_info_order(id_order: str) -> list:
#     logging.info(f'get_info_order')
#     values = order_sheet.get_all_values()
#     for i, item in enumerate(values):
#         if id_order in item:
#             return item
#     return False
#
#
# def get_key_product_office365(category: str) -> list:
#     logging.info(f'get_key_product_office365')
#     sheet = dict_category[category]
#     values = sheet.get_all_values()
#     list_key = []
#     for i, item in enumerate(values):
#         slice_item = item[:3]
#         slice_item.append(i)
#         list_key.append(slice_item)
#     return list_key
#
#
# def get_cost_product(product: str, typelink: str = 'None') -> list:
#     logging.info(f'get_cost_product, {product}:{typelink}')
#     values = cost_sheet.get_all_values()
#     cost_key = 0
#     product = product.strip()
#     for row, item in enumerate(values):
#         # print(item[:2], product in item[:3], 'online' in typelink, item[1] == 'online')
#         if product in item[:3] and 'online' in typelink and item[1] == 'online':
#             # print(1, item[4])
#             cost_key = item[3:7]
#             break
#         elif product in item[:3] and 'phone' in typelink and item[1] == 'phone':
#             # print(2, item[4])
#             cost_key = item[3:7]
#             break
#         elif product in item[:3] and 'linking' in typelink and item[1] == 'linking':
#             # print(3, item[4])
#             cost_key = item[3:7]
#             break
#         else:
#             if product == 'Office 365' and item[1] == 'None':
#                 cost_key = item[3:7]
#                 # print(4, item[4])
#                 break
#     # print(cost_key)
#     return cost_key
#
#
# def get_cost_product_list() -> list:
#     logging.info(f'get_cost_product_list')
#     values = cost_sheet.get_all_values()
#     list_cost_product = []
#     for product in values:
#         if product[0] == 'end':
#             break
#         else:
#             list_cost_product.append([product[0], product[1], product[3], product[4], product[5], product[6]])
#     # print(list_cost_product)
#     return list_cost_product
#
#
# # добавить значения
# def append_order(id_order, date, time, username, key, cost, category, product, type_give, id_product=-1):
#     """
#     Добавление нового заказа в таблицу order_sheet
#     :param id_order: токен заказ
#     :param date: дата заказа
#     :param time: время заказа
#     :param username: имя пользователя выполнившего заказ
#     :param key: выданный ключ
#     :param cost: стоимость ключа
#     :param category: категория ключа
#     :param product: продукт ключа
#     :param type_give: тип выдачи
#     :param id_product:
#     :return:
#     """
#     logging.info(f'append_order')
#     order_sheet.append_row([id_order, date, time, username, key, cost, category, product, type_give, id_product])
#
#
# def update_row_key_product_cancel(category: str, key: str) -> None:
#     """
#
#     :param category:
#     :param key:
#     :return:
#     """
#     logging.info(f'update_row_key_product_cancel: {key}')
#     # лист гугл-таблицы
#     sheet = dict_category[category]
#     # если категория = 'Office 365', так как эта категория содержит по одному ключу для активации
#     if category == 'Office 365':
#         # получаем все данные с листа
#         value_list = sheet.get_all_values()
#         # проходим по данным построчно
#         for i, row_value in enumerate(value_list):
#             # если ключ найден
#             if key in row_value[0]:
#                 # восстанавливаем его активацию
#                 sheet.update_cell(i+1, 2, '✅')
#     # остальные категории обрабатываются одинаково
#     else:
#         # поиск ключа на листе
#         cell = sheet.find(key)
#         # проходим по активациям
#         for i in range(7):
#             # находим ячейку, содержащую '❌' и меняем на '✅' и выходим из цикла
#             if sheet.cell(cell.row, cell.col+1+i).value == '❌':
#                 sheet.update_cell(cell.row, cell.col+1+i, '✅')
#                 break
#
#
# def update_row_key_product(category: str, id_product_in_category: int, id_key: int, change: bool = False,
#                            token_key: str = 'none') -> None:
#     """
#     Функция обновляет значение активации ключа
#     :param category:
#     :param id_product_in_category:
#     :param id_key:
#     :return:
#     """
#     logging.info(f'update_row_key_product')
#     sheet = dict_category[category]
#     values_list = sheet.row_values(id_key+1)[id_product_in_category*7:id_product_in_category*7+7]
#
#     if change:
#         if category == 'Office 365':
#             value_list = sheet.get_all_values()
#             for i, row_value in enumerate(value_list):
#                 if token_key in row_value[0]:
#                     sheet.update_cell(i + 1, 2, '⚠️')
#         else:
#             cell = sheet.find(token_key)
#             # print(cell.row, cell.col)
#             for i in range(7):
#                 # print(sheet.cell(cell.row, cell.col+1+i).value)
#                 if sheet.cell(cell.row, cell.col + 1 + i).value == '❌':
#                     sheet.update_cell(cell.row, cell.col + 1 + i, '⚠️')
#                     break
#
#     if id_product_in_category >= 0:
#
#         for i, value in enumerate(values_list):
#             if value == '✅':
#                 col = i + 7 * id_product_in_category
#                 # print(id_key+1, col)
#                 sheet.update_cell(id_key+1, col+1, '❌')
#                 break
#     else:
#         sheet.update_cell(id_key+1, 2, '❌')
#
#
# def delete_row_order(id_order: str) -> None:
#     logging.info(f'delete_row_order {id_order}')
#     cell = order_sheet.find(id_order)
#     order_sheet.delete_rows(cell.row)
#
#
# def update_row_order_listkey(id_order: str, listkey: str) -> None:
#     logging.info(f'delete_row_order {id_order}')
#     cell = order_sheet.find(id_order)
#     order_sheet.update_cell(cell.row, 5, listkey)
#
#
# def update_row_key_product_new_key(new_key:str, id_order: str) -> None:
#     """
#     Функция заносит ключ в таблицу заказов
#     :param new_key:
#     :param id_order:
#     :return:
#     """
#     logging.info(f'update_row_key_product_new_key')
#     values_list = order_sheet.get_all_values()
#     for row, order in enumerate(values_list):
#         if order[0] == id_order:
#             col = 11
#             if not order_sheet.cell(row+1, 11).value:
#                 order_sheet.update_cell(row+1, col, new_key)
#                 break
#             else:
#                 col += 1
#                 order_sheet.update_cell(row + 1, col, new_key)
#                 break
#
#
# # поиск строки и столбца положения значения
# def values_row_col():
#     values = office_sheet.get_all_values()
#     # print(values)
#
#
# def get_values_hand_product(product: str) -> str:
#     logging.info(f'get_values_hand_product')
#     values_list = cost_sheet.get_all_values()
#     cell = cost_sheet.find('Ключ по запросу')
#     # print(product)
#     for row, notes in enumerate(values_list[cell.row:]):
#         # print("product, notes[2]", product, notes[2])
#         if product in notes[2]:
#             # print(cell.row, cell.col)
#             # print(product, notes[3:7])
#             # print(cost_sheet.cell(row+22, 5).value)
#             return notes[3:7]
#         if notes[2] == '':
#             break
#
#
# def set_key_in_sheet(category: str, id_product_in_category: int, id_key: int, set_key: str, activate: int) -> None:
#     logging.info(f'set_key_in_sheet')
#     sheet = dict_category[category]
#     if category != 'Office 365':
#         col = 7 * id_product_in_category + 2
#     else:
#         col = 1
#     row = id_key + 1
#     print('col:', col, "row:", row)
#     sheet.update_cell(row=row, col=col, value=set_key)
#     for i in range(1, activate + 1):
#         sheet.update_cell(row=row, col=col + i, value='✅')
#
#
# def get_list_workday(id_telegram: int, month_work: int) -> list:
#     """
#     Получаем список смен текущего месяца
#     :param id_telegram:
#     :param month_work: месяц для которого получается список смен (0-будущий, 1-текущий)
#     :return:
#     """
#     logging.info(f'get_list_workday')
#     cell = work_sheet.find(str(id_telegram))
#     if cell is not None:
#         if work_sheet.cell(cell.row, 4-month_work).value is not None:
#             return work_sheet.cell(cell.row, 4-month_work).value.split(',')
#         else:
#             return [0]
#     else:
#         return [0]
#
#
# def set_list_workday(id_telegram: int, list_workday: str, username: str, month_work: int) -> None:
#     logging.info(f'set_list_workday')
#     cell = work_sheet.find(str(id_telegram))
#     if cell is not None:
#         work_sheet.update_cell(row=cell.row, col=4-month_work, value=list_workday)
#     else:
#         if month_work == 0:
#             work_sheet.append_row([str(id_telegram), username, 'none', list_workday])
#         else:
#             work_sheet.append_row([str(id_telegram), username, list_workday, 'none'])


if __name__ == '__main__':
    d = get_dict_working_shift(date='03.11.2024')
    print(d)
