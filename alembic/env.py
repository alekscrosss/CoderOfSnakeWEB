# файл env.py

from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context
from src.db.models import Base
from dotenv import load_dotenv
load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


sqlalchemy_url = os.environ.get('SQLALCHEMY_DATABASE_URL')

# URI: postgresql://username:password@domain:port/database


config.set_main_option("sqlalchemy.url", sqlalchemy_url)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:

    connectable = create_engine(sqlalchemy_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
