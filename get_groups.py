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
			utils.save_json_entities(dialog)

	utils.save_db_json_entities()

database.refresh_deleted_entities()