import telebot
import config
import utilities as u
import os
import graph as g
import chart as c
import currentcy as ch


bot = telebot.TeleBot(config.TOKEN)

key_words=["вернуться","ввод","вывод","баланс"]

default_outlay_cathegory = ['Еда', 'Транспорт', 'Связь', 'Досуг', 'Покупки', 'Здоровье','Другое','Вернуться']#доделать

default_profit_cathegory = ['Заработная плата','Дивиденды','Стипендия', 'Другое','Вернуться']

variants_of_output = {
    'out_profit': 'доходы',
    'out_outlay': 'расходы',
    'out_profit_and_outlay': 'доходы/расходы'
}
list_of_callbacks_to_start_input = ['in_profit', 'in_доход_no', 'in_outlay', 'in_расход_no']
start_message = 'Здравствуйте! Я Ваш спутник в мир управление финансами. ' \
                'С моей помощью Вы сможете контролировать свои доходы и выводить ' \
                'расходы в виде текста или графика. ' \
                'Это ещё далеко не всё, что я умею. Давайте начнём?'


with open("all_users.txt", 'r') as file_of_users: #Отправка стартового сообщения при перезагрузки бота (отключай когда тестишь))))
    list_of_users = file_of_users.readlines()
list_of_users.pop()
for i in list_of_users:
    bot.send_message(int(i), text=start_message, reply_markup=u.large_keyboard_creator(['Ввод', 'Вывод',"Баланс"]))


def input_curetsy_plus(message):
    if message.text.lower() in key_words:
         return 0
    with open(f'temp_input_of_{message.chat.id}.txt', 'r', encoding='utf-16') as f:
        try:
            name_of_operation = f.readline().split()[2]
            input_amount_plus(message)
            return 0
        except Exception:
             bot.send_message(message.chat.id, "Это не валюта")
             start_of_input(message)
    return 0


def input_money(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    except Exception:
        pass
    bot.send_message(message.chat.id, "Что будем вводить?",
                     reply_markup=u.small_keyboard_creator([["Доходы", "in_profit"], ["Расходы", 'in_outlay'],['Вернуться','return']]))


def output_money(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    except Exception:
        pass
    try:
        with open(f"{message.chat.id}.txt", 'r', encoding='utf-16') as file:
            f = file.read()
        bot.send_message(message.chat.id, "За какой промежуток времени выводим?",
                     reply_markup=u.small_keyboard_creator([["Неделя", 'out_week'], ["Месяц", "out_month"],['Вернуться','return']]))
    except:
        bot.send_message(message.chat.id,"Вы, к сожалению, еще ничего не ввели")
        send_welcome(message)

def input_cathegory_plus(message):
    cur_cath = message.text.lower()
    if cur_cath == 'вернуться':
        send_welcome(message)
        return 0
    u.add_to_file(message, f'{cur_cath}')
    with open(f'temp_input_of_{message.chat.id}.txt', 'r', encoding='utf-16') as file:
        line = file.readline()
        line = line.split()
    bot.send_message(message.chat.id,
                     f"Вы уверены, что хотите добавить {line[1]} в размере {line[3]} {line[2]} в категорию {line[4]}?",
                     reply_markup=u.small_keyboard_creator
                     ([['Да', 'in_profit_yes'], ['Исправить', f'in_{line[1]}_no']]))
    return 0


def input_amount_plus(message):
    cur_amo = message.text.lower()
    if cur_amo == 'вернуться':
        send_welcome(message)
        return 0
    try:
        cur_amo = round(float(cur_amo),2)
        u.add_to_file(message, f'{cur_amo}')

        with open(f'temp_input_of_{message.chat.id}.txt', 'r', encoding='utf-16') as file:
            line = file.readline()
            line = line.split()

            if line[1] == 'расход':
                list_of_cath = default_outlay_cathegory
            elif line[1] == 'доход':
                list_of_cath = default_profit_cathegory
            else:
                list_of_cath = default_profit_cathegory #заглушка

        bot.send_message(message.chat.id, "Теперь напишите категорию", reply_markup=u.large_keyboard_creator(list_of_cath,row=4))
        bot.register_next_step_handler(message, input_cathegory_plus)
        return 0

    except ValueError:
        bot.send_message(message.chat.id, "Это не число. Попробуйте еще раз ввести сумму дохода",
                         reply_markup=u.large_keyboard_creator(['Вернуться']))
        bot.register_next_step_handler(message, input_amount_plus)
        return 0


def start_of_input(message):
    msg = bot.send_message(message.chat.id, "Выберете валюту", reply_markup=u.small_keyboard_creator(
        u.list_to_matrix(['Рубли', 'Доллары', 'Евро', 'Вернуться'], ['₽', '$', '€', 'return'])))
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, reply_markup=None,
                          text=message.text)
    except Exception:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id-1, reply_markup=None,
                              text=message.text)




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, text=start_message, reply_markup=u.large_keyboard_creator(['Ввод', 'Вывод',"Баланс"]))
    with open("all_users.txt", "a+") as file:
        file.seek(0)
        a=file.readlines()
        if not (str(message.chat.id)+'\n' in a):
            file.write(str(message.chat.id)+'\n')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    except Exception:
        pass
    lower_message_text = message.text.lower()
    if lower_message_text == "ввод":
        input_money(message)
    elif lower_message_text == "вывод":
        output_money(message)
    elif lower_message_text == "баланс":
        try:
            with open(f"{message.chat.id}.txt", 'r', encoding='utf-16') as file:
                f = file.read()
            bot.send_message(message.chat.id, text="Ваш баланс: " + str(get_balance_without_date(message)) + " ₽")
        except:
            bot.send_message(message.chat.id, "Вы еще ничего не ввели")  # новый текст
        send_welcome(message)
    else:
        send_welcome(message)


@bot.callback_query_handler(func=lambda m: True)
def callbacks(call):
    if call.message:

        # Выход к началу
        if call.data == 'return':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                  text=call.message.text)
            send_welcome(call.message)

        # Ввод расходов
        # старт ввода расхода
        if call.data == 'in_outlay' or call.data == 'in_расход_no':
            with open(f'temp_input_of_{call.message.chat.id}.txt', 'w'):
                pass
            u.add_to_file(call.message, f'{call.message.date} расход ')

        # Ввод дохода
        # старт ввода дохода
        if call.data == 'in_profit' or call.data == 'in_доход_no':
            with open(f'temp_input_of_{call.message.chat.id}.txt', 'w'):
                pass
            u.add_to_file(call.message, f'{call.message.date} доход ')

        # Для всего ввода
        if call.data in list_of_callbacks_to_start_input:
            start_of_input(call.message)


        # ввод валюты
        if call.data == '₽' or call.data == '$' or call.data == '€':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                  text=call.message.text)
            cur_cur = call.data
            with open(f'temp_input_of_{call.message.chat.id}.txt', 'a', encoding='utf-16') as f:
                f.write(f'{cur_cur}' + ' ')
            with open(f'temp_input_of_{call.message.chat.id}.txt', 'r', encoding='utf-16') as f:
                name_of_operation = f.readline().split()[1]

            msg = bot.send_message(call.message.chat.id, f"Введите сумму {name_of_operation}а (только число)",
                                   reply_markup=u.large_keyboard_creator(['Вернуться']))
            bot.register_next_step_handler(msg, input_amount_plus)
        # Конец ввода
        if call.data == 'in_profit_yes':
            with open(f'temp_input_of_{call.message.chat.id}.txt', 'r', encoding='utf-16') as temp:
                t = temp.readline()

                logs = open(f'{call.message.chat.id}.txt', 'a', encoding='utf-16')
                logs.write(t + '\n')
                logs.close()
            os.remove(f'temp_input_of_{call.message.chat.id}.txt') #удаление файла (временный ввод)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                  text=call.message.text)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,text="Ваша запись успешно добавлена")
            send_welcome(call.message)

        # Вывод
        if call.data == 'out_month' or call.data == 'out_week':
            with open(f'temp_report_to_{call.message.chat.id}.txt', 'w'):
                pass
            bot.send_message(call.message.chat.id, "Что выводим?", reply_markup=u.small_keyboard_creator(
                u.list_to_matrix(['Доходы', 'Расходы', 'Доходы и расходы', 'Вернуться'],
                               ['out_profit', 'out_outlay', 'out_profit_and_outlay', 'return'])))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                  text=call.message.text)
        try:
            u.add_to_report(call.message, variants_of_output[call.data])
            if call.data=='out_profit':
                keyboard=u.small_keyboard_creator(
                u.list_to_matrix(['Текст',  'Вернуться'],
                               ['out_text', 'return']))
            elif call.data=='out_outlay':
                keyboard=u.small_keyboard_creator(
                u.list_to_matrix(['Текст', 'Диаграмма', 'Вернуться'],
                               ['out_text', 'out_chart', 'return']))
            else:
                keyboard=u.small_keyboard_creator(
                u.list_to_matrix(['Текст', 'График',  'Вернуться'],
                               ['out_text', 'out_graph', 'return']))

            bot.send_message(call.message.chat.id, "Выберете способ вывода?", reply_markup=keyboard)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                  text=call.message.text)
        except KeyError:
            pass

        if call.data == 'out_week':
            u.add_to_report(call.message, f"неделю ")

        if call.data == 'out_month':
            u.add_to_report(call.message, f"месяц ")

        if call.data == 'out_text' or call.data == 'out_graph' or call.data == 'out_chart':
            with open(f'temp_report_to_{call.message.chat.id}.txt', 'r', encoding='utf-16') as file:
                line = file.readline()
                line = line.split()


            # Определение временного промежутка

            cur_time = call.message.date
            if line[0] == 'неделю':
                min_time=-604800+cur_time #7 дней
            elif line[0] == 'месяц':
                min_time=-2592000+cur_time #30 дней
            else:
                min_time=-2592000+cur_time #30 дней заглушка

            matrix_of_data_base=u.file_to_matrix(f'{call.message.chat.id}.txt')

            matrix_with_correct_date=[]
            for i in matrix_of_data_base:
                if min_time<=int(i[0])<=cur_time:
                    matrix_with_correct_date.append(i)

            # Определение типа


            matrix_of_profits=[]
            matrix_of_outlays=[]


            final_sum_of_profits = 0
            final_sum_of_outlays = 0

            for i in matrix_with_correct_date:
                if i[1]=='доход':
                    matrix_of_profits.append(i)
                    final_sum_of_profits += ch.converter_to_RUB(i[2],float(i[3])) # надо сделать перевод
                else:# доделать возможны ошибки в будущем
                    matrix_of_outlays.append(i)
                    final_sum_of_outlays += ch.converter_to_RUB(i[2],float(i[3]))  # надо сделать перевод


            if line[1] == 'доходы':
                final_sum = final_sum_of_profits  #надо сделать перевод
            elif line[1] == 'расходы':
                final_sum = final_sum_of_outlays #надо сделать перевод
            else:
                final_sum = final_sum_of_profits-final_sum_of_outlays
            try:
                os.remove(f"temp_report_to_{call.message.chat.id}.txt") #удаление темп вывода
            except:
                pass
            if call.data == 'out_text':
                bot.send_message(call.message.chat.id, f"Ваши {line[1]} за {line[0]}: {final_sum}")  # доделать (вроде все)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                  text=call.message.text)
                send_welcome(call.message)

            if call.data == 'out_graph':
                if matrix_with_correct_date:
                    x=[int(matrix_with_correct_date[0][0])]
                    y=[0]
                    for i, t in enumerate(matrix_with_correct_date):
                        if t[1] == 'доход':
                            y.append(round(ch.converter_to_RUB(t[2],float(matrix_with_correct_date[i][3]))+float(y[i]),2))

                        elif t[1] == 'расход':
                            y.append(round(-1*ch.converter_to_RUB(t[2], float(matrix_with_correct_date[i][3])) + float(y[i]),2))
                        x.append(int(matrix_with_correct_date[i][0]))



                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                      text=call.message.text)
                    g.get_a_graph(x,y)
                    with open("temp_graph.png", 'rb') as chart:
                        bot.send_photo(call.message.chat.id, chart)
                    try:
                        os.remove("temp_graph.png")
                    except:
                        pass
                    send_welcome(call.message)

            if call.data == 'out_chart':
                vals=[0]*(len(default_outlay_cathegory)-1)
                for row_in_moo in matrix_of_outlays:
                    for k, j in enumerate(default_outlay_cathegory):
                        if row_in_moo[4].lower()==j.lower():
                            if row_in_moo[1]=="расход":
                                vals[k]+=ch.converter_to_RUB(row_in_moo[2],float(row_in_moo[3]))
                            break
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None,
                                      text=call.message.text)
                if c.get_a_chart(vals):
                    with open("temp_chart.png", 'rb') as chart:
                        bot.send_photo(call.message.chat.id, chart)
                    try:
                        os.remove("temp_chart.png")
                    except:
                        pass
                else:
                    bot.send_message(call.message.chat.id, "Недостаточно расходов за рассматриваемый промежуток времени")#новый текст
                send_welcome(call.message)







def get_balance_without_date(message):

    matrix_of_data_base = u.file_to_matrix(f'{message.chat.id}.txt')
    matrix_of_profits = []
    matrix_of_outlays = []

    final_sum_of_profits = 0
    final_sum_of_outlays = 0

    for i in matrix_of_data_base:
        if i[1] == 'доход':
            matrix_of_profits.append(i)
            final_sum_of_profits += ch.converter_to_RUB(i[2],float(i[3]))  # надо сделать перевод
        else:  # доделать возможны ошибки в будущем
            matrix_of_outlays.append(i)
            final_sum_of_outlays += ch.converter_to_RUB(i[2],float(i[3]))  # надо сделать перевод
        print(final_sum_of_profits,final_sum_of_outlays)
    return round(final_sum_of_profits - final_sum_of_outlays,2)

bot.infinity_polling()
