from peewee import Model
from peewee import SqliteDatabase
from peewee import IntegerField
from peewee import CharField
from peewee import TextField

from app import settings

stardict_db = SqliteDatabase("/home/jax/base/data/ecdict-sqlite-28/stardict.db", pragmas={
                             'journal_mode': 'wal'})
print(settings.SQLITEDB_FILE)
'''
CREATE TABLE "behavior" (
    "user_id"	INTEGER,
    "collect_dict_id"	TEXT,
    "like"	INTEGER NOT NULL DEFAULT 0,
    "is_junk"	INTEGER NOT NULL DEFAULT 0,
    "is_stop"	INTEGER NOT NULL DEFAULT 0,
    "is_core"	INTEGER NOT NULL DEFAULT 0,
    "is_done"	INTEGER NOT NULL DEFAULT 0,
    "search_count"	INTEGER NOT NULL DEFAULT 0,
    "last_search_at"	INTEGER NOT NULL DEFAULT 0,
    "repeat_count"	INTEGER NOT NULL DEFAULT 0,
    "remark"	TEXT NOT NULL DEFAULT "",
    PRIMARY KEY("user_id", "collect_dict_id")
)
'''


class Behavior(Model):
    user_id = IntegerField(column_name="user_id")
    collect_dict_id = IntegerField(column_name="collect_dict_id")
    like = IntegerField(column_name="like")
    is_junk = IntegerField(column_name="is_junk")
    is_stop = IntegerField(column_name="is_stop")
    is_core = IntegerField(column_name="is_core")
    is_done = IntegerField(column_name="is_done")
    search_count = IntegerField(column_name="search_count")
    last_search_at = IntegerField(column_name="last_search_at")
    repeat_count = IntegerField(column_name="repeat_count")
    remark = CharField(column_name="remark")

    class Meta:
        database = stardict_db
        table_name = 'behavior'

'''
CREATE TABLE "collect_dict" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "word"	TEXT NOT NULL DEFAULT "" UNIQUE,
    "kind_id"	INTEGER NOT NULL DEFAULT 0,
    "phonetic"	TEXT NOT NULL DEFAULT "",
    "definition"	TEXT NOT NULL DEFAULT "",
    "translation"	TEXT NOT NULL DEFAULT "",
    "nltk_type_id"	INTEGER NOT NULL DEFAULT 0,
    "create_at"	INTEGER NOT NULL DEFAULT 0
)
'''


class CollectDict(Model):
    id = IntegerField(column_name="id")
    word = CharField(column_name="word")
    phonetic = CharField(column_name="phonetic")
    definition = CharField(column_name="definition")
    translation = CharField(column_name="translation")
    nltk_short_type = CharField(column_name="nltk_short_type")
    nltk_type = CharField(column_name="nltk_type")
    nltk_type_name = CharField(column_name="nltk_type_name")
    create_at = IntegerField(column_name="create_at")

    class Meta:
        database = stardict_db
        table_name = 'collect_dict'


'''
CREATE TABLE "stop_words" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id"	INTEGER NOT NULL DEFAULT 0,
    "words"	TEXT NOT NULL DEFAULT "",
    "is_effective_word"	INTEGER NOT NULL DEFAULT 0,
    "enable"	INTEGER NOT NULL DEFAULT 0
)
'''


class StopWords(Model):
    user_id = IntegerField(column_name="user_id")
    words = CharField(column_name="words")
    is_effective_word = IntegerField(column_name="is_effective_word")
    enable = IntegerField(column_name="enable")

    class Meta:
        database = stardict_db
        table_name = 'stop_words'


'''
CREATE TABLE "user" (
    "user_id"	INTEGER,
    "user_name"	TEXT NOT NULL DEFAULT "",
    "desc"	TEXT NOT NULL DEFAULT "",
    PRIMARY KEY("user_id")
)
'''


class User(Model):
    user_id = IntegerField(column_name="user_id")
    user_name = CharField(column_name="user_name")
    desc = CharField(column_name="desc")

    class Meta:
        database = stardict_db
        table_name = 'user'


class StarDict(Model):
    word = CharField(column_name='word')
    phonetic = CharField(column_name='phonetic')
    definition = TextField(column_name='definition')
    translation = TextField(column_name='translation')
    pos = CharField(column_name="pos")

    class Meta:
        database = stardict_db
        table_name = 'stardict'