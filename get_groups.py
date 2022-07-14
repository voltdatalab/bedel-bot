from telethon import TelegramClient
import json
import database

api = None
with open("config.json") as jsonfile:
    api = json.load(jsonfile)['telegram']

with TelegramClient('anon', api['id'], api['hash']) as client:
	for dialog in client.iter_dialogs():
		if (dialog.entity.id > 0 and type(dialog.entity).__name__ != 'User'):
			database.update_entities(dialog)