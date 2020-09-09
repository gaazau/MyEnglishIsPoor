from peewee import *

database = SqliteDatabase('/home/jax/base/data/ecdict-sqlite-28/stardict.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

class Stardict(BaseModel):
    audio = TextField(null=True)
    bnc = IntegerField(null=True)
    collins = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    definition = TextField(null=True)
    detail = TextField(null=True)
    exchange = TextField(null=True)
    frq = IntegerField(null=True)
    oxford = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    phonetic = CharField(null=True)
    pos = CharField(null=True)
    sw = CharField()
    tag = CharField(null=True)
    translation = TextField(null=True)
    word = CharField(unique=True)

    class Meta:
        table_name = 'stardict'
        indexes = (
            (('sw', 'word'), False),
        )

