import json 
import database
import datetime

from PIL import Image

from simplediff import html_diff

from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os

def reset_json(file_name):
    with open('snapshot/'+file_name, 'w') as f:
        json.dump([], f, indent=4)

def save_json_entities(dialog):
    participants_count=dialog.entity.participants_count if hasattr(
        dialog.entity, 'participants_count') else 0
    telegram_id=str(dialog.entity.id)
    username=dialog.entity.username if hasattr(
            dialog.entity, 'username') else '-',
    verified=dialog.entity.verified if hasattr(
            dialog.entity, 'verified') else False,
    tipo=type(dialog.entity).__name__,
    broadcast=dialog.entity.broadcast if hasattr(
            dialog.entity, 'broadcast') else False,
    megagroup=dialog.entity.megagroup if hasattr(
            dialog.entity, 'megagroup') else False,
    gigagroup=dialog.entity.gigagroup if hasattr(
            dialog.entity, 'gigagroup') else False,
    name=dialog.entity.title if (type(dialog.entity).__name__ != 'User') else (dialog.entity.first_name if hasattr(dialog.entity, 'first_name') else "-" +
    " " + dialog.entity.last_name if hasattr(dialog.entity, 'last_name') else '-')
    
    new_entity = {
        "type": tipo[0],
        "telegram_id": telegram_id,
        "participants_count": participants_count, 
        "username": username[0], 
        "verified": verified[0], 
        "broadcast": broadcast[0], 
        "megagroup": megagroup[0],
        "gigagroup": gigagroup[0],
        "name": name
    }

    # append new_entity in a json file snapshot folder

    with open('snapshot/entities_new.json', 'r') as f:
        entities = json.load(f)
    entities.append(new_entity)
    with open('snapshot/entities_new.json', 'w') as f:
        json.dump(entities, f, indent=4)

def save_db_json_entities():
    old_entity = database.get_entities()

    for entity in old_entity:
        if entity.deleted is not True:
            new_entity = {
                "type": entity.type,
                "telegram_id": entity.telegram_id,
                "participants_count": entity.participants_count, 
                "username": entity.username, 
                "verified": entity.verified, 
                "broadcast": entity.broadcast, 
                "megagroup": entity.megagroup,
                "gigagroup": entity.gigagroup,
                "name": entity.name
            }
            with open('snapshot/entities_old.json', 'r') as f:
                entities = json.load(f)
            entities.append(new_entity)
            with open('snapshot/entities_old.json', 'w') as f:
                json.dump(entities, f, indent=4)

def save_json_messages(t_message):

    message_id=t_message.id,
    message=t_message.message,
    forwards=t_message.forwards,
    views=t_message.views,
    author=t_message.from_id.user_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'user_id') else t_message.from_id.channel_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'channel_id') else None,
    fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None,
    fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,
    fwd_from_type = type(t_message.fwd_from.from_id).__name__ if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,

    new_message = {
        "message_id": message_id[0],
        "message": message[0],
        "forwards": forwards[0],
        "views": views[0],
        "author": author[0],
        "fwd_from_id_message": fwd_from_id_message[0],
        "fwd_from_id": fwd_from_id[0],
        "fwd_from_type": fwd_from_type[0]
    }

    # append new_message in a json file snapshot folder

    with open('snapshot/messages_new.json', 'r') as f:
        entities = json.load(f)
    entities.append(new_message)
    with open('snapshot/messages_new.json', 'w') as f:
        json.dump(entities, f, indent=4)

def save_db_json_messages():
    old_messages= database.get_messages()

    for msg in old_messages:
        if msg.deleted is not True:
            new_message = {
                "message_id": msg.message_id,
                "message": msg.message,
                "forwards": msg.forwards,
                "views": msg.views,
                "author": msg.author,
                "fwd_from_id_message": msg.fwd_from_id_message,
                "fwd_from_id": msg.fwd_from_id,
                "fwd_from_type": msg.fwd_from_type
            }
            with open('snapshot/messages_old.json', 'r') as f:
                entities = json.load(f)
            entities.append(new_message)
            with open('snapshot/messages_old.json', 'w') as f:
                json.dump(entities, f, indent=4)

async def text_to_image(mensagem):

    old = mensagem.old_value if hasattr( mensagem, 'old_value') else ""
    new = mensagem.new_value if hasattr( mensagem, 'new_value') else ""
    data = str(mensagem.date) if hasattr( mensagem, 'date') else ""

    if hasattr( mensagem, 'date'):
        data = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        data -= datetime.timedelta(hours=3)
        data = data.strftime('%d/%m/%Y %H:%M:%S')
    
    data_deleted = str(mensagem.date_deleted) if hasattr( mensagem, 'date_deleted') else ""
    if hasattr( mensagem, 'deleted_at_date'):
        
        data_deleted = datetime.datetime.strptime(data_deleted, '%Y-%m-%d %H:%M:%S')
        data_deleted -= datetime.timedelta(hours=3)
        data_deleted = data_deleted.strftime('%d/%m/%Y %H:%M:%S')
    
    data += "\n** Esta Mensagem Foi Deletada: " + str(data_deleted)
    canal = mensagem.name if hasattr( mensagem, 'name') else ""

    if hasattr( mensagem, 'new_value'):
        texto = html_diff(old, new)
    else:
        texto = mensagem.message if hasattr( mensagem, 'message') else ""
    
    print((canal, texto, data))
    html = """

    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="css/styles.css">
    </head>
    <body>
    <p>
    <b> {} </b></br></br>
    {}
    </br>
    <small> {} </small>
    </p>
    </body>
    </html>
    """.format(canal, texto, data)

    with open('html/tmp.html', 'w') as f:
        f.write(html)

    firefoxOptions = Options()
    firefoxOptions.add_argument("-headless")

    driver = webdriver.Firefox(executable_path="./geckodriver", options=firefoxOptions)

    driver.get("file://" + os.getcwd() + "/html/tmp.html")

    e = driver.find_elements(By.XPATH, '//p')[0]
    start_height = int(e.location['y'])
    block_height = int(e.size['height'])
    end_height = int(start_height)
    start_width = int(e.location['x'])
    block_width = int(e.size['width'])

    end_width = int(start_width)
    total_height = int(start_height + block_height + end_height)
    total_width = start_width + block_width + end_width

    # print(start_height, block_height, end_height, start_width, block_width, end_width, total_height, total_width)

    driver.save_screenshot('html/tmp.png')

    img = Image.open('html/tmp.png')
    img2 = img.crop((0, 0, total_width, total_height))

    if int(total_width) > int(total_height * 2):
        background = Image.new('RGBA', (total_width, int(total_width / 2)),
                                (255, 255, 255, 0))
        bg_w, bg_h = background.size
        offset = (int((bg_w - total_width) / 2),
                int((bg_h - total_height) / 2))
    else:
        background = Image.new('RGBA', (total_width, total_height),
                                (255, 255, 255, 0))
        bg_w, bg_h = background.size
        offset = (int((bg_w - total_width) / 2),
                int((bg_h - total_height) / 2))
    background.paste(img2, offset)

    background.save('html/out.png')

def get_urls(t_message):
    url = []
    if (hasattr(t_message, 'entities') and t_message.entities is not None):

        for i in t_message.entities:
            if (hasattr(i, 'url') and i.url is not None):
                url.append(i.url)
            else:
                url_tmp = t_message.message[i.offset:i.offset + i.length]

                if (url_tmp.startswith('http')):
                    url.append(url_tmp)
    
    return url

def date_format(message):
    if type(message) is datetime:
        return message.strftime("%Y-%m-%d %H:%M:%S")