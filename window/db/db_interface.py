from db.models import Behavior
from db.models import Post
from db.models import StopWords
from db.models import WordList


class DbInterface(object):
    def __init__(self):
        self.db = SqliteInterface()

    def get_stop_words(self):
        return self.db.get_stop_words()

class SqliteInterface(object):
    def get_stop_words(self):
        query = StopWords.select(StopWords.word)
        stop_words = [row.word for row in query]
        return stop_words