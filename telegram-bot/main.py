import telebot
from telebot import types
from datetime import datetime, date, time
import psycopg2


token = "5076189420:AAH_bXqMWqHk7x8-QYY2vF_dA0N31xIB4sI"

bot = telebot.TeleBot(token)


conn = psycopg2.connect(database="timetable",
                        user="nikiforova.olesya",
                        password="123456",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


start = date(2021, 9, 1)
d = datetime.now()
week = d.isocalendar()[1] - start.isocalendar()[1] + 1


if week % 2 == 0:
    top_week = True
    text_week = "нижней/четной"
else:
    top_week = False
    text_week = "верхней/нечетной"


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/help", "/MTUCI", "/week")
    keyboard.row("понедельник", "четверг")
    keyboard.row("вторник", "пятница")
    keyboard.row("среда", "суббота")
    keyboard.row("расписание на эту неделю")
    keyboard.row("расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Здравствуйте, ' + message.from_user.first_name + '! ' +
                     'Чтобы узнать, что умеет бот, напишите /help', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/MTUCI - информация о ВУЗе\n' +
                     '/week\n' +
                     'понедельник\n' +
                     'вторник\n' +
                     'среда\n' +
                     'четверг\n' +
                     'пятница\n' +
                     'суббота\n' +
                     'расписание на эту неделю\n' +
                     'расписание на следующую неделю')


@bot.message_handler(commands=['MTUCI'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Тогда вам сюда – https://mtuci.ru/')


@bot.message_handler(commands = ['week'])
def week(message):
    if top_week:
        bot.send_message(message.chat.id, 'нижняя/четная неделя')
    else:
        bot.send_message(message.chat.id, 'верхняя/нечетная неделя')


@bot.message_handler()
def answer(message):
    weeks = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
    if message.text.lower() in weeks:
        if message.text.lower() == "понедельник":
            dd = 1
            text_day = "понедельник"
        elif message.text.lower() == "вторник":
            dd = 2
            text_day = "вторник"
        elif message.text.lower() == "среда":
            dd = 3
            text_day = "среду"
        elif message.text.lower() == "четверг":
            dd = 4
            text_day = "четверг"
        elif message.text.lower() == "пятница":
            dd = 5
            text_day = "пятницу"
        elif message.text.lower() == "суббота":
            dd = 6
            text_day = "субботу"
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = {dd} and top_week = {top_week}\
                        ORDER BY schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на {text_day} (по {text_week} неделе):")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")

    elif message.text.lower() == "расписание на эту неделю":
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 1 and top_week = {top_week}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        print(records)
        bot.send_message(message.chat.id, f"Расписание на эту неделю:")
        bot.send_message(message.chat.id, f"Понедельник")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 2 and top_week = {top_week}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Вторник")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 3 and top_week = {top_week}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Среда")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 4 and top_week = {top_week}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Четверг")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 5 and top_week = {top_week}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Пятница")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 6 and top_week = {top_week}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Суббота")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")

    elif message.text.lower() == "расписание на следующую неделю":
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 1 and top_week = {not(top_week)}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        print(records)
        bot.send_message(message.chat.id, f"Расписание на следующую неделю:")
        bot.send_message(message.chat.id, f"Понедельник")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 2 and top_week = {not(top_week)}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Вторник")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 3 and top_week = {not(top_week)}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Среда")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 4 and top_week = {not(top_week)}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Четверг")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 5 and top_week = {not(top_week)}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Пятница")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
        cursor.execute(f'SELECT subject.subject_name, schedule.classroom, schedule.start_time, teacher.full_name, schedule.day\
                        FROM subject\
                        INNER JOIN schedule ON subject.id = schedule.subject_fk\
                        INNER JOIN teacher ON subject.id = teacher.subject_fk\
                        WHERE day = 6 and top_week = {not(top_week)}\
                        ORDER BY schedule.day, schedule.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Суббота")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")

    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понял. Воспользуйтесь командой /help :)')


bot.polling()
