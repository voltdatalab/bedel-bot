import json 
import database

def reset_json(file_name):
    with open('snapshot/'+file_name, 'w') as f:
        json.dump([], f, indent=4)


def save_json(dialog):
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

def save_db_json():
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
