from alchemy import Entity, EntityChange, Message, Media, MessageChange
from json import load
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


# Criando tabelas
with open("config.json") as jsonfile:
    config = load(jsonfile)
    env = config['env']

    if env == "dev":
        db_config = config['database_dev']
        engine = create_engine(db_config['drivername'], echo=True)

    if env == "prod":
        db_config = config['database']
        engine = create_engine(URL.create(db_config['drivername'], db_config['username'], db_config['password'], db_config['host'],
                                  db_config['port'], db_config['database']), 
								  connect_args={'options': '-csearch_path={}'.format(db_config['schema'])})

Entity.__table__.create(bind=engine, checkfirst=True)
EntityChange.__table__.create(bind=engine, checkfirst=True)
Message.__table__.create(bind=engine, checkfirst=True)
MessageChange.__table__.create(bind=engine, checkfirst=True)
Media.__table__.create(bind=engine, checkfirst=True)

