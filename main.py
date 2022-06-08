import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from bot import send_msg

with open('pythonProject/token.txt') as file:
    token = file.readline()

vk = vk_api.VkApi(token=token)
session_api = vk.get_api()
longpoll = VkLongPoll(vk)


def searh(text):
    places = ['7 шк', 'пожарк', 'таремско', 'лини', 'юж', 'редгум', 'кочк', 'башн', 'ред гум', 'шашлычк',
              'заправк', 'ждан', 'редгум', 'фок', 'мерид', 'молявино', 'автосуш', 'авто суш', 'реан',
              'низ', 'базар', 'централ', 'тумботино', 'налог', 'линии', '66 гараж']
    actions = ['стоят', 'палк', 'веста', 'стоит', 'работа', 'встали']
    fl1, fl2 = False, False
    for place in places:
        if place in text:
            fl1 = True
            break
    for action in actions:
        if action in text:
            fl2 = True
            break
    if fl1 and fl2:
        return True


def send_message(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})

# send_message('234776693', 'ghgh')

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.user_id == 213813749:
        if searh(event.text):
            print(event.text)
            send_msg(234776693, event.text)
        else:
            print(1)
    else:print(2)



