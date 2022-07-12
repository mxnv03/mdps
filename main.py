import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_token, bot_token
from datetime import datetime
import telebot, getpass
from telebot import types


# инициализация бота тг
USER_NAME = getpass.getuser()
bot = telebot.TeleBot(token=bot_token)

# инициализация вк
vk = vk_api.VkApi(token=vk_token)
session_api = vk.get_api()
longpoll = VkLongPoll(vk)

users_now = []  # пользователи, участвующие в рассылке
places = ['7', 'dkgkg', 'flgl']  # мдпс в настоящий момент
last_ten_messages = []

def searh(text):  # основная функция
    places = ['7 шк', 'пожарк', 'таремско', 'лини', 'юж', 'редгум', 'кочк', 'башн', 'ред гум', 'шашлычк',
              'заправк', 'ждан', 'редгум', 'фок', 'мерид', 'молявино', 'автосуш', 'авто суш', 'реан',
              'низ', 'базар', 'централ', 'тумботино', 'налог', 'линии', '66 гар', 'пап', '66']
    # actions = ['стоят', 'палк', 'веста', 'стоит', 'работа', 'встали']
    actions = ['чисто']
    fl1, fl2 = False, True
    for place in places:
        if place in text:
            fl1 = True
            break
    for action in actions:
        if action in text:
            fl2 = False
            break
    if fl1 and fl2:
        return True


def places_form(pl):  # красивая выдача запроса об мдпс
    msg = 'Чуваки возможно чиллят тут: \n'
    for i in range(len(pl)):
        msg += f'❕ {pl[i]} \n'
    return msg

def correct_last_ten_messages(msg):
    global last_ten_messages
    now = datetime.now()
    if len(last_ten_messages) < 10:
        last_ten_messages += [now.strftime("%H:%M"), msg]
    else:
        last_ten_messages.pop(0)
        last_ten_messages += [now.strftime("%H:%M"), msg]
    message = 'Вот последние 10 сообщений: \n'
    for i in range(len(last_ten_messages)):
        message += f'{last_ten_messages[i][0]} {last_ten_messages[i][1]}' + '/n'


@bot.message_handler(commands=['start'])  # реагирование на команду /start
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Включить оповещения")
    btn2 = types.KeyboardButton("Возможное МДПС в настоящий момент")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот,"
                                           " который будет помогать тебе избежать "
                                           "штрафов!".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):  # ответы на сообщения бота
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
        bot.send_message(message.chat.id, text="Рассылка выключена!"
                                               "\nНе забудьте включить её :)".format(message.from_user),
                         reply_markup=markup)
    elif text == 'возможное мдпс в настоящий момент':
        bot.send_message(message.from_user.id, places_form(places))
    elif text == 'показать последние 10 сообщений':
        try:
            bot.send_message(message.from_user.id, last_ten_messages)
        except telebot.apihelper.ApiTelegramException:
            print('okk')
    elif text == 'рассылка':
        for i in range(len(users_now)):
            bot.send_message(users_now[i], places_form(places))


    else:
        bot.send_message(message.from_user.id, 'Упс, что-то пошло не так...')


bot.polling()  # прослушивание запросов пользователя тг бота

for event in longpoll.listen():  #прослушивание лс в вк
    if event.type == VkEventType.MESSAGE_NEW and event.peer_id == 2000000000+240:
        correct_last_ten_messages(msg=event.text)
        if searh(event.text.lower()):
            places += [event.text]
            for id in range(len(users_now)):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Выключить оповещения")
                btn2 = types.KeyboardButton("Возможное МДПС в настоящий момент")
                btn3 = types.KeyboardButton("Показать последние 10 сообщений")
                markup.add(btn1, btn2, btn3)
                bot.send_message(users_now[id], text=event.text,
                                 reply_markup=markup)
        else:
            print(12344)
            for id in range(len(users_now)):
                bot.send_message(users_now[id], event.text)

    elif event.type == VkEventType.MESSAGE_NEW:
        print(1234556)
        #sender(234776693, '2')


