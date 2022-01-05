import telebot
from telebot import types

token = "2109478366:AAGU37wkvs7rmD8BqXmTF69WFaR8vdn5Wbs"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/help", "/MTUCI", "/timetable")
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '! ' +
                     'Чтобы узнать, что умеет бот, пиши /help', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/MTUCI - информация о ВУЗе\n' +
                        '/timetable - узнай расписание\n' +
                        'мтуси соц.сети - официальные страницы сообщества\n' +
                        'активист мтуси - официальные страницы сообщества Студенческой жизни\n' +
                        'погода - узнай, какая сегодня погода')


@bot.message_handler(commands=['MTUCI'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')


@bot.message_handler(commands=['timetable'])
def schedule(message):
    bot.send_message(message.chat.id, 'Расписание всех академических групп – https://mtuci.ru/time-table/')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "мтуси соц.сети":
        bot.send_message(message.chat.id, 'Группа VK: https://vk.com/mtuci/\n' +
                         'Instagram: https://www.instagram.com/mtuci.official/')
    elif message.text.lower() == "активист мтуси":
        bot.send_message(message.chat.id, 'Группа VK: https://vk.com/aktivist_mtuci/\n' +
                         'Instagram: https://www.instagram.com/aktivist_mtuci/')
    elif message.text.lower() == "погода":
        bot.send_message(message.chat.id, 'Узнай погоду на сегодня – https://yandex.ru/pogoda/')


bot.polling()