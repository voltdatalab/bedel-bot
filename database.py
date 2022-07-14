from html import entities
import json
import datetime
import conn

from sqlalchemy import create_engine, func
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from alchemy import Entity, EntityChange, Message, Media

engine = conn.run()

def update_entities(dialog):
    Session = sessionmaker(bind=engine)
    session = Session()

    old_entity = session.query(Entity).filter_by(
        telegram_id=str(dialog.entity.id)).filter_by(type=type(dialog.entity).__name__).first()

    if (old_entity):

        # Novas variaveis
        participants_count=dialog.entity.participants_count if hasattr(
            dialog.entity, 'participants_count') else 0
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
        
        old_entity.verified = dialog.entity.verified if hasattr(
            dialog.entity, 'verified') else False

        old_entity.participants_count = dialog.entity.participants_count if hasattr(
            dialog.entity, 'participants_count') else 0

        new_entity = {
            "type": tipo[0],
            "participants_count": participants_count, 
            "username": username[0], 
            "verified": verified[0], 
            "broadcast": broadcast[0], 
            "megagroup": megagroup[0],
            "gigagroup": gigagroup[0],
            "name": name
        }

        changes = []
        # Compara se existe diferenças e coloca em Changes
        for key, value in vars(old_entity).items():
            if key in new_entity:
                dialog_value = new_entity[key]
                if dialog_value != value:
                    changes.append((key, value, dialog_value))

        print(changes)
        
        # Adiciona changes na tabela EntityChange
        for change in changes:
            session.add(EntityChange(
                entity_id=old_entity.id,
                date = datetime.datetime.now(),
                attr_name=change[0],
                old_value=change[1],
                new_value=change[2]
            ))
        
        # append new_entity in a json file snapshot folder

        # with open('snapshot/entities.json', 'r') as f:
        #     entities = json.load(f)
        # entities.append(new_entity)
        # with open('snapshot/entities.json', 'w') as f:
        #     json.dump(entities, f, indent=4)
 
    else:
        new_entity = Entity(type=type(dialog.entity).__name__,
                            telegram_id=str(dialog.entity.id),
                            participants_count=dialog.entity.participants_count if hasattr(
            dialog.entity, 'participants_count') else 0,
            username=dialog.entity.username if hasattr(
                dialog.entity, 'username') else '-',
            verified=dialog.entity.verified if hasattr(
                dialog.entity, 'verified') else False,
            broadcast=dialog.entity.broadcast if hasattr(
                dialog.entity, 'broadcast') else False,
            megagroup=dialog.entity.megagroup if hasattr(
                dialog.entity, 'megagroup') else False,
            gigagroup=dialog.entity.gigagroup if hasattr(
                dialog.entity, 'gigagroup') else False,
            name=dialog.entity.title if (type(dialog.entity).__name__ != 'User') else
            (dialog.entity.first_name if hasattr(dialog.entity, 'first_name') else "-" +
             " " + dialog.entity.last_name if hasattr(dialog.entity, 'last_name') else '-')
        )

        session.add(new_entity)
        session.flush()

    session.commit()
    session.close()

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
    old_entity = get_entities()

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

def refresh_deleted():
    import pandas as pd

    Session = sessionmaker(bind=engine)
    session = Session()

    df_db = pd.read_json('snapshot/entities_old.json')
    df_tel = pd.read_json('snapshot/entities_new.json')

    diff_set = set(df_db["telegram_id"].values) ^ set(df_tel["telegram_id"].values)

    for entity_id in diff_set:
        print("\n--Atualizado entity_id: " + str(entity_id))
        entity = session.query(Entity).filter_by(telegram_id=str(entity_id)).first()
        
        print(entity.name)
        entity.deleted = True
        entity.deleted_at_date = datetime.datetime.now().date()

    session.commit()
    session.close()

def get_entities():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(Entity).all()

def get_last_id(dialog):
    Session = sessionmaker(bind=engine)
    session = Session()

    db_entity = session.query(Entity).filter_by(
        telegram_id=str(dialog.entity.id)).first()
    result = session.query(func.max(Message.message_id)).filter_by(entity_id=db_entity.id).first()

    session.close()
    
    return result

def get_first_id(dialog, days_qty):
    Session = sessionmaker(bind=engine)
    session = Session()

    db_entity = session.query(Entity).filter_by(telegram_id=str(dialog.entity.id)).first()
    result = session.query(func.min(Message.message_id)).filter_by(entity_id=db_entity.id).filter(
        Message.date > datetime.date.today() - datetime.timedelta(days=days_qty)).first()

    session.close()

    return result

def save_message(dialog, t_message):
    Session = sessionmaker(bind=engine)
    session = Session()

    db_entity = session.query(Entity).filter_by(telegram_id=str(dialog.entity.id)).first()

    old_message = session.query(Message).filter_by(entity_id=db_entity.id).filter(Message.message_id == t_message.id).first()

    if (old_message):
        old_message.forwards = t_message.forwards
        old_message.views = t_message.views
        old_message.message = t_message.message
        old_message.edit_date = t_message.editdate if hasattr(t_message, 'editdate') else None
        old_message.fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None
        old_message.fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None

    else: 
        new_message = Message(
            message_id=t_message.id,
            message=t_message.message,
            entity_id=db_entity.id,
            date=t_message.date,
            edit_date=t_message.editdate if hasattr(
                t_message, 'editdate') else None,
            forwards=t_message.forwards,
            views=t_message.views,
            author=t_message.from_id.user_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'user_id') else t_message.from_id.channel_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'channel_id') else None,
            fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None,
            fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,
            fwd_from_type = type(t_message.fwd_from.from_id).__name__ if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,

        )

        session.add(new_message)
        session.flush()

        if hasattr(t_message.media, 'document'):
            new_media = Media(
                message_id = new_message.id,
                media_id = t_message.media.document.id,
                access_hash = t_message.media.document.access_hash,
                file_reference = t_message.media.document.file_reference,
                date = t_message.media.document.date,
                mime_type = t_message.media.document.mime_type
            )

            session.add(new_media)

    session.commit()
    session.close()

def date_format(message):
    if type(message) is datetime:
        return message.strftime("%Y-%m-%d %H:%M:%S")