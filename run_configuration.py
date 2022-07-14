from alchemy import Entity, EntityChange, Message, Media, MessageChange
from json import load
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import conn

engine = conn.run()

Entity.__table__.create(bind=engine, checkfirst=True)
EntityChange.__table__.create(bind=engine, checkfirst=True)
Message.__table__.create(bind=engine, checkfirst=True)
MessageChange.__table__.create(bind=engine, checkfirst=True)
Media.__table__.create(bind=engine, checkfirst=True)

