from telethon.sync import TelegramClient
import json
import database
import utils
import datetime

api = None
with open("config.json") as jsonfile:
    api = json.load(jsonfile)['telegram']

utils.reset_json('messages_new.json')
utils.reset_json('messages_old.json')

with TelegramClient('anon', api['id'], api['hash']) as client:

    entities = database.get_entities()
    entities = [entity for entity in entities if entity.deleted is not True]

    for entity in entities:

        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))

        if entity.telegram_id == api['channel_response']:
            continue
        
        print("--- entity.telegram_id ", str(entity.telegram_id))
        telegram_messages = client.get_messages(entity.telegram_id, limit = 50000)
        print("+++")

        database.save_messages(entity.telegram_id, telegram_messages)

        # for message in client.iter_messages(entity.telegram_id):

        #     # print(message)
        #     # database.save_message(entity.telegram_id, message)
        #     utils.save_json_messages(message)
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
    utils.save_db_json_messages() #

database.refresh_deleted_messages() 