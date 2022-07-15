import json 
import database
import datetime

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


def date_format(message):
    if type(message) is datetime:
        return message.strftime("%Y-%m-%d %H:%M:%S")