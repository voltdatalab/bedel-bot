
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import json
import utils
from telethon import TelegramClient
import emoji

from alchemy import TrendingToday, SuperTrendingToday
import conn

with open("config.json") as jsonfile:
    api = json.load(jsonfile)['telegram']

engine = conn.run()

async def send_to_telegram(mensagem):
    content = "Nome do Canal: " + mensagem.name if mensagem.name else ""
    content += ("\nMensagem: " + emoji.emojize(mensagem.message) if hasattr( mensagem, 'message') else "")
    print(content)
    try:
        await utils.text_to_image(mensagem)
        content = "Nome do Canal: " + mensagem.name if mensagem.name else ""
        await client.send_message(api['channel_response'], content, file='html/out.png')

    except Exception as e:
        print("Erro ao enviar mensagem para o Telegram: {}".format(e))

        texto = "Nome do Canal: " + mensagem.name if mensagem.name else ""
        texto += "\n\n"
        texto += mensagem.message if hasattr( mensagem, 'message') else ""

        await client.send_message(api['channel_response'], texto)

async def send():
    
    Session = sessionmaker(bind = engine)
    session = Session()
    result_trending_today = session.query(TrendingToday).all()
    result_super_trending_today = session.query(SuperTrendingToday).all()

    if len(result_trending_today) > 0:
        head_line = '**🚀 Trendings Diarias ----- **\n'
        await client.send_message(api['channel_response'], head_line)

    for row in result_trending_today:
        if row.message == '' or row.message == None: continue
        print ("Name: ",row.name, " Message: ",row.message)
        print("-------------------------------------------\n")
        await send_to_telegram(row)

    if len(result_super_trending_today) > 0:
        head_line = '**🔥 Super Trendings Diarias ----- **\n'
        await client.send_message(api['channel_response'], head_line)

    for row in result_super_trending_today:
        if row.message == '' or row.message == None: continue
        print ("Name: ",row.name, " Message: ",row.message)
        print("-------------------------------------------\n")
        await send_to_telegram(row)
    
    if len(result_trending_today) > 0 or len(result_super_trending_today) > 0:
        head_line = '**------- 😉 FIM dos Trendings Diarias ----- **\n'
        await client.send_message(api['channel_response'], head_line)
    
client = TelegramClient('anon', api['id'], api['hash'])

with client:
    client.loop.run_until_complete(send())

