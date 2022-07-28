from json import load
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

def run():
# Criando tabelas
    with open("config.json") as jsonfile:
        config = load(jsonfile)
        env = config['env']

        if env == "dev":
            db_config = config['database_dev']
            engine = create_engine(db_config['drivername'], echo=False)

        if env == "prod":
            db_config = config['database']
            engine = create_engine(URL.create(db_config['drivername'], db_config['username'], db_config['password'], db_config['host'],
                                    db_config['port'], db_config['database']), 
                                    connect_args={'options': '-csearch_path={}'.format(db_config['schema'])})

    return engine