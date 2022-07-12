import telebot, keyboa, pyautogui, getpass
from telebot import types
from config import bot_token


USER_NAME = getpass.getuser()
bot = telebot.TeleBot(token=bot_token)
users_now = []
places = ['7', 'dkgkg', 'flgl']


def places_form(pl):
    msg = 'Чуваки возможно чиллят тут: \n'
    for i in range(len(pl)):
        msg += f'❕ {pl[i]} \n'
    return msg


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Включить оповещения")
    btn2 = types.KeyboardButton("Возможное МДПС в настоящий момент")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот,"
                                           " который будет помогать тебе избежать "
                                           "штрафов!".format(message.from_user), reply_markup=markup)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.lower()
    if text == 'включить оповещения':
        if message.chat.id not in users_now:
            users_now.append(message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выключить оповещения")
        btn2 = types.KeyboardButton("Возможное МДПС в настоящий момент")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Ok, рассылка включена!".format(message.from_user), reply_markup=markup)
    elif text == 'выключить оповещения':
        if message.chat.id in users_now:
            users_now.pop(users_now.index(message.chat.id))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Включить оповещения")
        btn2 = types.KeyboardButton("Возможное МДПС в настоящий момент")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Рассылка выключена! "
                                               "\n Не забудьте включить её :)".format(message.from_user),
                         reply_markup=markup)
    elif text == 'возможное мдпс в настоящий момент':
        bot.send_message(message.from_user.id, places_form(places))
    elif text == 'рассылка':
        for i in range(len(users_now)):
            bot.send_message(users_now[i], places_form(places))


    else:
        bot.send_message(message.from_user.id, 'Упс, что-то пошло не так...')

bot.polling()
