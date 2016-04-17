from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cells = Table('cells', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('x', Integer),
    Column('y', Integer),
    Column('type_name', String),
    Column('f', Integer),
    Column('g', Integer),
    Column('i', Integer),
    Column('c', Integer),
    Column('culture', String),
    Column('allaince', String),
    Column('player_name', String),
    Column('population', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cells'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cells'].drop()
