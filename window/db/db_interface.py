from db.models import Behavior
from db.models import Post
from db.models import StopWords
from db.models import WordList
from db.models import Stardict


class DbInterface(object):
    def __init__(self):
        self.db = SqliteInterface()

    def get_stop_words(self):
        return self.db.get_stop_words()

    def get_words_detail(self, words):
        star_word_dict = self.db.get_words_detail(words)
        return star_word_dict

    def save_word_list(self, word_data):
        if not word_data:
            return True
        return self.db.save_word_list(word_data)

    def get_done_word_list(self, word_list):
        return self.db.get_done_word_list(word_list)

    def save_behavior(self, behavior_data):
        if not behavior_data:
            return True
        return self.db.save_behavior(behavior_data)

    def save_stop_words(self, stop_word_data):
        if not stop_word_data:
            return True
        return self.db.save_stop_words(stop_word_data)


class SqliteInterface(object):
    def get_stop_words(self):
        query = StopWords.select(StopWords.word)
        stop_words = [row.word for row in query]
        return stop_words

    def get_words_detail(self, words):
        query = Stardict.select(
            Stardict.word,
            Stardict.phonetic,
            Stardict.definition,
            Stardict.translation,
        ).where(Stardict.word.in_(words))
        words_dict = {}
        # key ignore Caps
        for row in query:
            words_dict[row.word.lower()] = {
                'word': row.word.lower(),
                'phonetic': row.phonetic,
                'definition': row.definition,
                'translation': row.translation
            }
        return words_dict

    def save_word_list(self, words_list):
        query = WordList.insert_many(words_list).on_conflict('replace').execute()
        return query > 0

    def get_done_word_list(self, word_list):
        query = WordList.select(
            WordList.word
        ).join(
            Behavior,
            on=(Behavior.word == WordList.word)
        ).where(WordList.word.in_(word_list), Behavior.word_statu > 0)
        return [row.word for row in query]

    def save_behavior(self, behavior_data):
        query = Behavior.insert_many(behavior_data).on_conflict('replace').execute()
        return query > 0

    def save_stop_words(self, stop_word_data):
        query = StopWords.insert_many(stop_word_data).on_conflict('replace').execute()
        return query > 0