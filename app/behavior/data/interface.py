from datetime import datetime

from app.behavior.data.model import Behavior
from app.behavior.data.model import User
from app.behavior.data.model import CollectDict
from app.behavior.data.model import StopWords

from peewee import *


class BehaviorInterface(object):
    def get_user_info(self, user_id):
        query = User.select(
            User.user_id,
            User.user_name,
            User.desc,
        ).where(User.user_id == user_id)
        return query

    def get_word_detail(self, words_list):
        query = StarDict.select(
            StarDict.word,
            StarDict.phonetic,
            StarDict.definition,
            StarDict.translation
        ).where(
            StarDict.word.in_(words_list))
        return query

    def get_user_dict_record(self, user_id):
        query = Behavior.select(
            Behavior.user_id,
            Behavior.collect_dict_id,
            Behavior.like,
            Behavior.is_junk,
            Behavior.is_stop,
            Behavior.is_core,
            Behavior.is_done,
            Behavior.search_count,
            Behavior.last_search_at,
            Behavior.repeat_count,
            Behavior.remark,
            CollectDict.word,
            CollectDict.kind_id,
            CollectDict.phonetic,
            CollectDict.definition,
            CollectDict.translation,
            CollectDict.nltk_type_id,
            CollectDict.create_at,
        ).join(
            CollectDict, on=(CollectDict.id == Behavior.collect_dict_id)
        ).where(Behavior.user_id == user_id)
        return query

    def get_stop_words(self, user_ids):
        query = StopWords.select(
            StopWords.user_id,
            StopWords.words,
            StopWords.is_effective_word,
            StopWords.enable,
        ).where(StopWords.user_id.in_(user_ids))
        return query

    def get_collection_words(self, user_id, words_list)
    query = CollectDict.select(
        CollectDict.id,
        CollectDict.word,
        CollectDict.kind_id,
        CollectDict.phonetic,
        CollectDict.definition,
        CollectDict.translation,
        CollectDict.nltk_type_id,
        CollectDict.batch_id，
        CollectDict.create_at,
    ).where(CollectDict.user_id == user_id, CollectDict.word.in_(words_list))
    return query


class DBWorker(object):
    def __init__(self):
        self.db_api = BehaviorInterface()

    """数据库操作"""

    def get_stop_words(self, user_ids):
        if not user_ids:
            return []
        query = self.db_api.get_stop_words(user_ids)
        stop_words_list = [row.words for row in query]
        return stop_words_list

    def get_words_detail(self, words_list):
        return self.db_api.get_word_detail(words_list)

    def get_history_words(self, user_id):
        if not user_id:
            return []
        return self.db_api.get_user_dict_record(user_id)

    def get_words_in_history(self, user_id, words_list):
        if not user_id or not words_list:
            return []
        query = self.db_api.get_collection_words(user_id, words_list)
        return [row['word'] for row in query]

    def insert_words_into_collect_dict(self, user_id, words_list):
        words_data = []
        now_ts = int(datetime.now().timestamp())
        for row in words_list:
            words_data.append({
                "word": row['word'],
                "word_kind": "",
                "phonetic": row['phonetic'],
                "definition": row['definition'],
                "translation": row['translation'],
                "nltk_short_type": row['short_type'],
                "batch_id": now_ts,
                "create_at": now_ts,
            })
        return True

    def update_user_behavior(self, user_id,  collection_id, is_done, is_stop):
        Behavior.create(
            user_id=user_id,
            collect_dict_id=collection_id,
            is_done=is_done,
            is_stop=is_stop,
            last_search_at=int(datetime.now().timestamp())
        )
        return Ture

    def get_word_collection(self, user_id, words):
        return self.db_api.get_collection_words(user_id, words)

if __name__ == "__main__":
    inf = BehaviorInterface()
    # query = inf.get_user_info(1001)
    # print(query)
    # query = inf.get_user_record(1001, [1])
    # print(query)
    # query = inf.get_word_detail(['apple'])
    # print(query)
    query = inf.get_user_behavior_record(1001)
    print(query)
