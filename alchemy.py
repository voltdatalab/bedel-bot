from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Entity(Base):
    __tablename__ = 'telegram_entities'

    id = Column(Integer, primary_key=True)
    type = Column(Text)
    telegram_id = Column(Integer)
    name = Column(Text)
    participants_count = Column(Integer)
    username = Column(Text)
    broadcast = Column(Boolean)
    verified = Column(Boolean)
    megagroup = Column(Boolean)
    gigagroup = Column(Boolean)
    deleted = Column(Boolean)
    deleted_at_date = Column(DateTime)

    def __repr__(self):
        return f'Entity {self.name}'

class EntityChange(Base):
    __tablename__ = 'telegram_entity_changes'

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("telegram_entities.id"), nullable=False)
    date = Column(DateTime)
    attr_name = Column(Text)
    old_value = Column(Text)
    new_value = Column(Text)

    def __repr__(self):
        return f'EntityChange {self.attr_name}'

class Message(Base):
    __tablename__ = 'telegram_messages'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, index=True)
    message = Column(Text)
    entity_id = Column(Integer, ForeignKey("telegram_entities.id"), nullable=False)
    date = Column(DateTime)
    forwards = Column(Integer)
    views = Column(Integer)
    author = Column(Integer)
    fwd_from_type = Column(Text)
    fwd_from_id = Column(Integer)
    fwd_from_id_message = Column(Integer)
    deleted = Column(Boolean)
    deleted_at_date = Column(DateTime)

    UniqueConstraint('message_id', 'entity_id', name='unique_message')

    def __repr__(self):
        return f'Message {self.message}'

class MessageChange(Base):
    __tablename__ = 'telegram_message_changes'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("telegram_messages.id"), nullable=False)
    date = Column(DateTime)
    attr_name = Column(Text)
    old_value = Column(Text)
    new_value = Column(Text)
    addition = Column(Text)
    removal = Column(Text)

    def __repr__(self):
        return f'MessageChange {self.attr_name}'

class Urls(Base):
    __tablename__ = 'telegram_urls'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("telegram_messages.id"), nullable=False)
    url = Column(Text)

    def __repr__(self):
        return f'Url {self.url}'


class Reaction(Base):
    __tablename__ = 'telegram_reactions'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("telegram_messages.id"), nullable=False)
    emoji = Column(Text)
    count = Column(Integer)

    def __repr__(self):
        return f'reaction: {self.emoji} {self.count}'



class Media(Base):
    __tablename__ = 'telegram_medias'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("telegram_messages.id"), nullable=False)
    media_id = Column(Text)
    access_hash = Column(Text)
    file_reference = Column(Text)
    date = Column(DateTime)
    mime_type = Column(Text)
    backup_link = Column(Text)

    def __repr__(self):
        return f'Media {self.file_reference}'



class TrendingToday(Base):
   __tablename__ = 'trending_today'
   id = Column(Integer, primary_key =  True)
   message_id = Column(Integer)
   message = Column(String)
   name = Column(String)
   entity_id = Column(Integer)

   date = Column(DateTime)
   forwards = Column(Integer)
   views = Column(Integer)

class SuperTrendingToday(Base):
   __tablename__ = 'super_trending_today'
   id = Column(Integer, primary_key =  True)
   message_id = Column(Integer)
   message = Column(String)
   name = Column(String)
   entity_id = Column(Integer)

   date = Column(DateTime)
   forwards = Column(Integer)
   views = Column(Integer)
