from peewee import *

database = SqliteDatabase('window/db/my_words.db')


class BaseModel(Model):
    class Meta:
        database = database

class Behavior(BaseModel):
    word = TextField(null=True, primary_key=True)
    word_statu = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'behavior'

class Post(BaseModel):
    create_at = IntegerField(constraints=[SQL("DEFAULT 0")])
    detail = TextField(constraints=[SQL("DEFAULT ''")])
    title = TextField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'post'

class PostWords(BaseModel):
    post_id = IntegerField(null=True)
    word = TextField(null=True)

    class Meta:
        table_name = 'post_words'
        indexes = (
            (('post_id', 'word'), True),
        )
        primary_key = CompositeKey('post_id', 'word')


class StopWords(BaseModel):
    word = TextField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = 'stop_words'

class WordList(BaseModel):
    definition = IntegerField(constraints=[SQL("DEFAULT ''")])
    phonetic = IntegerField(constraints=[SQL("DEFAULT ''")])
    translation = IntegerField(constraints=[SQL("DEFAULT ''")])
    word = TextField(null=True, primary_key=True)
    word_type = IntegerField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'word_list'




############################

database2 = SqliteDatabase('/home/jax/base/data/ecdict-sqlite-28/stardict.db')

class BaseModel2(Model):
    class Meta:
        database = database2

class Stardict(BaseModel2):
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
        
############################