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
