from asyncore import read
from telethon import TelegramClient
import json
import database
import utils


api = None
with open("config.json") as jsonfile:
    api = json.load(jsonfile)['telegram']


utils.reset_json('entities_new.json')
utils.reset_json('entities_old.json')

with TelegramClient('anon', api['id'], api['hash']) as client:

	dialogs = client.iter_dialogs()
	for dialog in client.iter_dialogs():
		if (dialog.entity.id > 0 and type(dialog.entity).__name__ != 'User'):

			database.update_entities(dialog)
			database.save_json(dialog)

	database.save_db_json()

database.refresh_deleted()