from db.models import Behavior
from db.models import Post
from db.models import StopWords
from db.models import WordList
from db.models import Stardict
from db.models import PostWords
from datetime import datetime


from peewee import fn


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

    def save_post(self, title, url, post_hash):
        return self.db.save_post(title, url, post_hash)

    def save_post_words(self, post_data):
        if not post_data:
            return True
        return self.db.save_post_words(post_data)

    def get_posts(self):
        return self.db.get_posts()

    def get_post(self, post_id):
        return self.db.get_post(post_id)

    def get_post_word_data(self, post_id):
        return self.db.get_post_word_data(post_id)

    def get_post_words_unique(self, post_id):
        words = self.db.get_post_words(post_id)
        return self.db.get_post_words_count(words)

    def delete_post(self, post_id):
        return self.db.delete_post(post_id)

    def delete_post_words(self, post_id):
        return self.db.delete_post_words(post_id)

    def delete_behavior(self, words):
        return self.db.delete_behavior(words)

    def delete_word_list(self, words):
        return self.db.delete_word_list(words)


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
        query = WordList.insert_many(
            words_list).on_conflict('replace').execute()
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
        query = Behavior.insert_many(
            behavior_data).on_conflict('replace').execute()
        return query > 0

    def save_stop_words(self, stop_word_data):
        query = StopWords.insert_many(
            stop_word_data).on_conflict('replace').execute()
        return query > 0

    def save_post(self, title, url, post_hash):
        return Post.insert(title=title, url=url, post_hash=post_hash, create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')).execute()

    def save_post_words(self, post_data):
        return PostWords.insert_many(post_data).execute()

    def get_posts(self):
        query = Post.select(
            Post.id,
            Post.title,
            Post.url,
        ).order_by(Post.create_at.desc())
        post_list = []
        for row in query:
            post_list.append({
                'id': row.id,
                'title': row.title,
                'url': row.url,
                'create_at': row.create_at,
            })
        return post_list

    def get_post(self, post_id):
        query = Post.select(
            Post.id,
            Post.title,
            Post.url,
            Post.create_at,
        ).where(Post.id == post_id)
        for row in query:
            return {
                "id": row.id,
                "title": row.title,
                "url": row.url,
                "create_at": row.create_at,
            }
        return None

    def get_post_word_data(self, post_id):
        query = PostWords.select(
            PostWords.post_id,
            PostWords.word,
            WordList.definition,
            WordList.phonetic,
            WordList.translation,
            WordList.word,
            WordList.word_type,
            Behavior.word_statu
        ).join(
            WordList,
            on=(PostWords.word == WordList.word)
        ).join(
            Behavior,
            on=(PostWords.word == Behavior.word)
        ).where(
            PostWords.post_id == post_id
        ).dicts()
        return [row for row in query]

    def get_post_words(self, post_id):
        query = PostWords.select(
            PostWords.word
        ).where(
            PostWords.post_id == post_id
        )
        return [row.word for row in query]

    def get_post_words_count(self, words):
        query = PostWords.select(
            PostWords.word
        ).where(
            PostWords.word.in_(words)
        ).group_by(
            PostWords.word
        ).having(fn.Count(PostWords.word) == 1)
        print(query)
        return [row.word for row in query]

    def delete_post(self, post_id):
        query = Post.delete().where(
            Post.id == post_id
        ).execute()

    def delete_post_words(self, post_id):
        PostWords.delete().where(
            PostWords.post_id == post_id
        ).execute()

    def delete_behavior(self, words):
        Behavior.delete().where(
            Behavior.word.in_(words)
        ).execute()

    def delete_word_list(self, words):
        WordList.delete().where(
            WordList.word.in_(words)
        ).execute()
