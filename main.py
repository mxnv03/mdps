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
    for i in range(len(places)):
        if places[i].lower() in text:
            return True


def send_message(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})

# send_message('234776693', 'ghgh')

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == 240:
        if searh(event.text):
            send_msg(234776693, event.text)



