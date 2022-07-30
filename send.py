
from sqlalchemy import create_engine, func
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import json
import utils
from telethon import TelegramClient
import datetime
import emoji

from alchemy import Entity, Message, MessageChange
import conn

with open("config.json") as jsonfile:
    api = json.load(jsonfile)['telegram']

async def send_to_telegram(mensagem):
    content = "Nome do Canal: " + mensagem.name if mensagem.name else ""
    content += ("\nMensagem: " + emoji.emojize(mensagem.message) if hasattr( mensagem, 'message') else "")
    content += ("\nDe: " + emoji.emojize(mensagem.old_value) if hasattr( mensagem, 'old_value') else "")
    content += ("\nPara: " + emoji.emojize(mensagem.new_value) if hasattr( mensagem, 'new_value') else "")
    content += ("\nDeletado em: " + str(mensagem.deleted_at_date) if hasattr( mensagem, 'deleted_at_date') and mensagem.deleted_at_date != None  else "")

    # await client.send_message(354322347, content)
    await utils.text_to_image(mensagem)
    await client.send_message(api['channel_response'], content, file='html/out.png')
    # await client.send_message('me', content)

def send_to_twitter(mensagem):
    pass

async def send(filter_date):
    engine = conn.run()

    Session = sessionmaker(bind=engine)
    session = Session()

    # Modificadas e Deletadas
    query = session.query(
            MessageChange.message_id, 
            func.max(MessageChange.date).label('date'), 
            Entity.name, 
            MessageChange.attr_name, 
            MessageChange.old_value, 
            MessageChange.new_value,
            Message.deleted,
            Message.deleted_at_date
            ).join(
                Message, Message.id == MessageChange.message_id
            ).join(
                Entity, Entity.id == Message.entity_id
            ).filter(
                MessageChange.attr_name == 'message',
                MessageChange.date >= filter_date
            ).group_by(
                MessageChange.message_id,
                Entity.name, 
                MessageChange.attr_name, 
                MessageChange.old_value, 
                MessageChange.new_value,
                Message.deleted,
                Message.deleted_at_date
            ).all()

    # Apenas as deletadas
    query_just_deleted = session.query(
        Entity.name, 
        Message.message,
        Message.deleted_at_date
        ).outerjoin(
            MessageChange, 
            Message.id == MessageChange.message_id
        ).join(
            Entity, Entity.id == Message.entity_id
        ).filter(
            MessageChange.id == None, 
            Message.date >= filter_date,
            Message.deleted != None
        ).all()

    for row in query:
        await send_to_telegram(row)
        send_to_twitter(row)

        print('+------------------------')
        print("|Grupo {}".format(row.name))
        print("|\t De:  {} ".format(row.old_value))
        print("|\t Para:  {} ".format(row.new_value))
        if row.deleted:
            print("|\t Deletado em:  {} ".format(row.deleted_at_date))
        print('+------------------------\n')

    for row in query_just_deleted:
        await send_to_telegram(row)
        send_to_twitter(row)

        print('\n+-----------------')
        print("|Grupo: {}".format(row.name))
        print("|Mensagem Deletada: {}".format(row.message))
        print("|Deletado em: {}".format(row.deleted_at_date))
        print('+----------------\n')

client = TelegramClient('anon', api['id'], api['hash'])

with client:

    filter_date = datetime.datetime.now(datetime.timezone.utc)
    filter_date -= datetime.timedelta(hours=4)
    
    print("\n\n Filtrando as mensagens de {}".format(filter_date))

    client.loop.run_until_complete(send(filter_date))