import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

with open('pythonProject/bot_token.txt') as file:
    token = file.readline()

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

users_now = []

def send_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})
