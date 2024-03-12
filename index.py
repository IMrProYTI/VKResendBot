from threading import Thread

from dotenv import load_dotenv
import os

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')
TG_GROUP = os.getenv('TG_GROUP')
VK_TOKEN = os.getenv('VK_TOKEN')
VK_GROUP = os.getenv('VK_GROUP')


import telebot
bot = telebot.TeleBot(TG_TOKEN)


import vk_api
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def findTheBest(attachments_media: list):
	I = 0
	_max = attachments_media['photo']['sizes'][0]['width']

	for i in range(1, len(attachments_media)):
		width = attachments_media['photo']['sizes'][i]['width']
		if _max < width:
			I = i
			_max = width
	
	return attachments_media['photo']['sizes'][I]['url']


while True:
	vk_session = VkApi(token=VK_TOKEN)
	longpoll = VkBotLongPoll(vk_session, group_id=VK_GROUP)
	for event in longpoll.listen():
		try:
			if event.type == VkBotEventType.WALL_POST_NEW:
				TEXT = event.obj.text
				if len(TEXT) > 1024:
					for media in event.obj.attachments:
						bot.send_photo(TG_GROUP, findTheBest(media))
					bot.send_message(TG_GROUP, TEXT)
				else:
					for i in range(len(event.obj.attachments)):
						media = event.obj.attachments[i]
						if len(event.obj.attachments)-1 == i:
							bot.send_photo(TG_GROUP, findTheBest(media), TEXT)
						else:
							bot.send_photo(TG_GROUP, findTheBest(media))
		except Exception:
			pass

if __name__ == '__main__':
	thread = [
		Thread(target=bot.infinity_polling)
	]
	for t in thread:
		t.start()