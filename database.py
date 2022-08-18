import datetime
import conn
import emoji

from sqlalchemy import create_engine, func
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from simplediff import string_diff

from alchemy import Entity, EntityChange, Message, MessageChange, Media, Urls
import utils

engine = conn.run()

def get_media_type(mensagem_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    media = session.query(Media).filter_by(message_id=mensagem_id).first()
    return media.mime_type if media else None

# ENTITIES STUFF
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
        
        # old_entity.verified = dialog.entity.verified if hasattr(
        #     dialog.entity, 'verified') else False

        # old_entity.participants_count = dialog.entity.participants_count if hasattr(
        #     dialog.entity, 'participants_count') else 0

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

        # if ( str( old_entity.id ) == '5'):
        #     print(dialog.id)
        #     input("ola")
        
        # Adiciona changes na tabela EntityChange
        for change in changes:
            session.add(EntityChange(
                entity_id=old_entity.id,
                date = datetime.datetime.now(datetime.timezone.utc),
                attr_name=change[0],
                old_value=change[1],
                new_value=change[2]
            ))
        
        # Atualizar old_entity com novos dados
        old_entity.name = new_entity["name"]
        old_entity.type = new_entity["type"]
        old_entity.participants_count = new_entity["participants_count"]
        old_entity.username = new_entity["username"]
        old_entity.verified = new_entity["verified"]
        old_entity.broadcast = new_entity["broadcast"]
        old_entity.megagroup = new_entity["megagroup"]
        old_entity.gigagroup = new_entity["gigagroup"]

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

def refresh_deleted_entities():
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
        entity.deleted_at_date = datetime.datetime.now(datetime.timezone.utc)

    session.commit()
    session.close()

def get_entities():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(Entity).all()


# MESSSAGES STUFF
def save_message(id, t_message):

    print("\n\n -- Salvando mensagem: " + str(id))
    print(len(t_message.entities))

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    db_entity = session.query(Entity).filter_by(telegram_id=str(id)).first()

    old_message = session.query(Message).filter_by(entity_id=db_entity.id).filter(Message.message_id == t_message.id).first()

    if (old_message):
        # Novas varaiveis
        message_id=t_message.id,
        message=t_message.message,
        entity_id=db_entity.id,
        date=t_message.date,
        # edit_date=t_message.editdate if hasattr(
        #     t_message, 'editdate') else None,
        forwards=t_message.forwards,
        views=t_message.views,
        author=t_message.from_id.user_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'user_id') else t_message.from_id.channel_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'channel_id') else None,
        fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None,
        fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,
        fwd_from_type = type(t_message.fwd_from.from_id).__name__ if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,

        new_message = {
            "message_id": message_id[0],
            "message": message[0],
            "entity_id": entity_id[0],
            # "date": date[0],
            # "edit_date": edit_date[0],
            "forwards": forwards[0],
            "views": views[0],
            "author": author[0],
            "fwd_from_id_message": fwd_from_id_message[0],
            "fwd_from_id": fwd_from_id[0],
            "fwd_from_type": fwd_from_type[0]
        }

        # old_message.update(new_message)

        changes = []
        # Compara se existe diferenças e coloca em Changes
        for key, value in vars(old_message).items():
            if key in new_message:
                dialog_value = new_message[key]
                if dialog_value != value:
                    changes.append((key, value, dialog_value))

        # Adiciona changes na tabela EntityChange
        for change in changes:
            session.add(MessageChange(
                message_id=old_message.id,
                date = t_message.edit_date if t_message.edit_date else datetime.datetime.now(datetime.timezone.utc),
                attr_name=change[0],
                old_value=change[1],
                new_value=change[2],
            ))
        
        old_message.forwards = t_message.forwards
        old_message.views = t_message.views
        old_message.message = emoji.demojize(t_message.message)
        # old_message.edit_date = t_message.edit_date if t_message.edit_date else None
        old_message.fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None
        old_message.fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None

    else: 
        new_message = Message(
            message_id=t_message.id,
            message=emoji.demojize(t_message.message),
            entity_id=db_entity.id,
            date=t_message.date,
            # edit_date=t_message.editdate if hasattr(
            # t_message, 'editdate') else None,

            forwards=t_message.forwards,
            views=t_message.views,
            author=t_message.from_id.user_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'user_id') else t_message.from_id.channel_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'channel_id') else None,
            fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None,
            fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,
            fwd_from_type = type(t_message.fwd_from.from_id).__name__ if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,

        )

        session.add(new_message)

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
        session.flush()

    session.commit()
    session.close()


def save_messages(id, t_messages):
    print("--- Entrou no Save messages ---")
    Session = sessionmaker(bind=engine)
    session = Session()

    db_entity = session.query(Entity).filter_by(telegram_id=str(id)).first()

    for t_message in t_messages:
        print('-Save Message -', t_message.id)

        old_message = session.query(Message).filter_by(entity_id=db_entity.id).filter(Message.message_id == t_message.id).first()

        start_date = '2022-06-15'
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

        t_message_date = str(t_message.date.date())
        now_date = datetime.datetime.strptime(t_message_date, '%Y-%m-%d')

        if (now_date < start_date):
            break

        if (old_message):
            # Novas varaiveis
            message_id=t_message.id,
            message=emoji.demojize(t_message.message) if t_message.message else "",
            entity_id=db_entity.id,
            date=t_message.date,

            forwards=t_message.forwards,
            views=t_message.views,
            author=t_message.from_id.user_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'user_id') else t_message.from_id.channel_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'channel_id') else None,
            fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None,
            fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,
            fwd_from_type = type(t_message.fwd_from.from_id).__name__ if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,

            new_message = {
                "message_id": message_id[0],
                "message": message[0],
                "entity_id": entity_id[0],
                "forwards": forwards[0],
                "views": views[0],
                "author": author[0],
                "fwd_from_id_message": fwd_from_id_message[0],
                "fwd_from_id": fwd_from_id[0],
                "fwd_from_type": fwd_from_type[0]
            }

            # old_message.update(new_message)

            changes = []
            # Compara se existe diferenças e coloca em Changes
            for key, value in vars(old_message).items():
                if key in new_message:
                    dialog_value = new_message[key]
                    if dialog_value != value:
                        if key == "message":
                            print("a: " + value + str(type(value)))
                            print("b: " + dialog_value + str(type(dialog_value)))
                        changes.append((key, value, dialog_value))

            # Adiciona changes na tabela MessageChange
            for change in changes:
                diff = None
                if change[0] == 'message':
                    diff = string_diff(change[1], change[2])
                    string_add = ' | '.join([' '.join(d[1]) for d in diff if d[0] == '+'])
                    string_del = ' | '.join([' '.join(d[1]) for d in diff if d[0] == '-'])

                session.add(MessageChange(
                    message_id=old_message.id,
                    date = t_message.edit_date if t_message.edit_date and change[0] == 'message' else datetime.datetime.now(datetime.timezone.utc),
                    attr_name=change[0],
                    old_value=change[1],
                    new_value=change[2],
                    addition = string_add if diff else None,
                    removal = string_del if diff else None
                ))
            
            old_message.forwards = t_message.forwards
            old_message.views = t_message.views
            old_message.message = emoji.demojize(t_message.message) if t_message.message else ""
            old_message.fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None
            old_message.fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None

        else: 
            new_message = Message(
                message_id=t_message.id,
                message=emoji.demojize(t_message.message) if t_message.message else "",
                entity_id=db_entity.id,
                date=t_message.date,
                forwards=t_message.forwards,
                views=t_message.views,
                author=t_message.from_id.user_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'user_id') else t_message.from_id.channel_id if hasattr(t_message, 'from_id') and hasattr(t_message.from_id, 'channel_id') else None,
                fwd_from_id_message = t_message.fwd_from.channel_post if t_message.fwd_from is not None and t_message.fwd_from.channel_post is not None else None,
                fwd_from_id = list(vars(t_message.fwd_from.from_id).values())[0] if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,
                fwd_from_type = type(t_message.fwd_from.from_id).__name__ if t_message.fwd_from is not None and t_message.fwd_from.from_id is not None else None,

            )

            # get id of new message in session
            session.add(new_message)
            session.flush() 
        
            print("id do novo message: " + str(new_message.id))

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
                session.flush() 

            urls = utils.get_urls(t_message)
            if urls:
                for url in urls:
                    new_url = Urls(
                        message_id=new_message.id,
                        url=url,
                    )
                    session.add(new_url)
                    session.flush() 
    

        session.flush() 
        session.commit()
        utils.save_json_messages(t_message)
    
    session.close()

def get_messages():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(Message).all()

def refresh_deleted_messages():
    import pandas as pd

    Session = sessionmaker(bind=engine)
    session = Session()

    df_db = pd.read_json('snapshot/messages_old.json')
    df_tel = pd.read_json('snapshot/messages_new.json')

    diff_set = set(df_db["message_id"].values) ^ set(df_tel["message_id"].values)
    print("DIFF SET")
    print(diff_set)
    for message_id in diff_set:
        print("\n--Atualizado message_id: " + str(message_id))
        message = session.query(Message).filter_by(message_id=str(message_id)).first()
        
        print(message.message)
        message.deleted = True
        message.deleted_at_date = datetime.datetime.now(datetime.timezone.utc)

    session.commit()
    session.close()
