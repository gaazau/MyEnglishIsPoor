from peewee import *

database = SqliteDatabase('window/db/my_words.db')


class BaseModel(Model):
    class Meta:
        database = database

class Behavior(BaseModel):
    is_done = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_mark = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_stop = IntegerField(constraints=[SQL("DEFAULT 0")])
    word_list_id = AutoField(null=True)

    class Meta:
        table_name = 'behavior'

class Post(BaseModel):
    create_at = IntegerField(constraints=[SQL("DEFAULT 0")])
    detail = TextField(constraints=[SQL("DEFAULT ''")])
    title = TextField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'post'

class StopWords(BaseModel):
    word = TextField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = 'stop_words'

class WordList(BaseModel):
    definition = TextField(constraints=[SQL("DEFAULT ''")])
    phonetic = TextField(constraints=[SQL("DEFAULT ''")])
    post_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    translation = TextField(constraints=[SQL("DEFAULT ''")])
    word = FloatField(constraints=[SQL("DEFAULT ''")], index=True)
    word_type = TextField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'word_list'

