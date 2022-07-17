from telethon.sync import TelegramClient
import json
import database
import utils


api = None
with open("config.json") as jsonfile:
    api = json.load(jsonfile)['telegram']

utils.reset_json('messages_new.json')
utils.reset_json('messages_old.json')

with TelegramClient('anon', api['id'], api['hash']) as client:

    entities = database.get_entities()
    entities = [entity for entity in entities if entity.deleted is not True]

    for entity in entities:
        database.save_messages(entity.telegram_id, client.get_messages(entity.telegram_id, limit = 50000))
        for message in client.iter_messages(entity.telegram_id):
            # print(message)
            # database.save_message(entity.telegram_id, message)
            utils.save_json_messages(message)

    utils.save_db_json_messages() #

database.refresh_deleted_messages() 