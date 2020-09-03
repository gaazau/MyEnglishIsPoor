from datetime import datetime

from app.behavior.data.model import Behavior
from app.behavior.data.model import User
from app.behavior.data.model import CollectDict
from app.behavior.data.model import StopWords
from app.behavior.data.model import StarDict


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
        max_at = Behavior.select(Behavior.last_search_at)
        query = Behavior.select(
            Behavior.user_id,
            Behavior.collect_dict_id,
            Behavior.is_stop,
            Behavior.is_done,
            Behavior.last_search_at,
            CollectDict.word,
            CollectDict.phonetic,
            CollectDict.definition,
            CollectDict.translation,
            CollectDict.nltk_short_type,
            CollectDict.nltk_type,
            CollectDict.nltk_type_name,
            CollectDict.create_at,
        ).join(
            CollectDict, on=(CollectDict.id == Behavior.collect_dict_id)
        ).where(Behavior.user_id == user_id, Behavior.last_search_at==max_at).dicts()
        return query

    def get_stop_words(self, user_ids):
        query = StopWords.select(
            StopWords.user_id,
            StopWords.words,
            StopWords.is_effective_word,
            StopWords.enable,
        ).where(StopWords.user_id.in_(user_ids))
        return query

    def get_collection_words(self, words_list):
        query = CollectDict.select(
            CollectDict.id,
            CollectDict.word,
            CollectDict.phonetic,
            CollectDict.definition,
            CollectDict.translation,
            CollectDict.nltk_short_type,
            CollectDict.nltk_type,
            CollectDict.nltk_type_name,
            CollectDict.create_at,
        ).where(CollectDict.word.in_(words_list))
        return query

    def insert_to_collection(self, word_list):
        return CollectDict.insert_many(word_list).execute()

    def insert_to_behavior(self, behavior_data):
        return Behavior.insert_many(behavior_data).execute()

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
        word_dict = {}
        for row in self.db_api.get_word_detail(words_list):
            word_dict[row.word.lower()] = row
        return word_dict

    def get_history_words(self, user_id):
        if not user_id:
            return []
        return self.db_api.get_user_dict_record(user_id)

    def get_words_in_history(self, user_id, words_list):
        if not user_id or not words_list:
            return []
        query = self.db_api.get_collection_words(user_id, words_list)
        return [row['word'] for row in query]

    def insert_words_into_collect_dict(self, words_list):
        if not words_list:
            return True
        words_data = []
        now_ts = int(datetime.now().timestamp())
        for row in words_list:
            words_data.append({
                "word": row['word'],
                "phonetic": row['phonetic'],
                "definition": row['definition'],
                "translation": row['translation'],
                "nltk_short_type": row['short_type'],
                "nltk_type": row['type'],
                "nltk_type_name": row['name'],
                "create_at": now_ts,
            })
        
        return self.db_api.insert_to_collection(words_data)
    
    def insert_to_behavior(self, user_id, word_ids):
        if not word_ids:
            return True
        now_ts = int(datetime.now().timestamp())
        behavior_data = []
        for word_id in word_ids:
            behavior_data.append({
                'user_id':user_id,
                'collect_dict_id':word_id,
                'last_search_at': now_ts
            })
        return self.db_api.insert_to_behavior(behavior_data)

    def get_word_collection(self, words):
        return self.db_api.get_collection_words(words)

    def get_user_dict_record(self, user_id):
        return self.db_api.get_user_dict_record(user_id)