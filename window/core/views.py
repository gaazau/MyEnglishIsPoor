import re
import settings
from nltk import word_tokenize
from nltk import pos_tag
from copy import deepcopy
from db.db_interface import DbInterface


class Views(object):
    def extract_english_words(self, content):
        """提取英文单词"""
        if not content:
            return []
        return sorted(set(re.findall(re.compile(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)*"), content)))

    def exclude_stop_words(self, src_words, stop_words):
        if not stop_words or not src_words:
            return src_words
        new_words = []
        for word in src_words:
            if word in stop_words:
                continue
            new_words.append(word)
        return new_words

    def get_word_type_dict(self, words_list):
        tokens = word_tokenize("\n".join(words_list))
        tags = pos_tag(tokens)
        tags_dict = {}
        for tag in tags:
            tags_dict[tag[0]] = tag[1]
        return tags_dict

    def save_word_list(self, word_list, behavior_list, post_dict):
        word_data = []
        behavior_data = []
        stop_word_data = []
        for i, row in enumerate(word_list):
            if 0 <= behavior_list[i] < 2:
                word_data.append({
                    'word': row[0],
                    'translation': row[1],
                    'phonetic': row[2],
                    'definition': row[3],
                    'word_type': row[4],
                })
                behavior_data.append({
                    'word': row[0],
                    'word_statu': behavior_list[i],
                })
            else:
                stop_word_data.append({
                    'word': row[0]
                })
        DbInterface().save_word_list(word_data)
        DbInterface().save_behavior(behavior_data)
        DbInterface().save_stop_words(stop_word_data)
        try:
            post_words = "\n".join(sorted({row['word'] for row in word_data}))
            post_id = DbInterface().save_post(
                post_dict['title'], post_dict['url'], str(hash(post_words)))
        except Exception:
            post_id = None
        if post_id:
            post_data = []
            for row in word_data:
                post_data.append({
                    'post_id': post_id,
                    'word': row['word'],
                })
            DbInterface().save_post_words(post_data)
        return post_id

    def delete_post_words(self, post_id):
        if not post_id:
            return True
        words = DbInterface().get_post_words_unique(post_id)
        DbInterface().delete_post(post_id)
        DbInterface().delete_post_words(post_id)
        if words:
            DbInterface().delete_behavior(words)
            DbInterface().delete_word_list(words)

    def get_post_words(self, txt_post):
        origin_words = self.extract_english_words(txt_post)
        if not origin_words:
            return []
        stop_words = DbInterface().get_stop_words()
        clean_words = self.exclude_stop_words(origin_words, stop_words)
        return clean_words


class GlobalData():
    word_list_header = ['单词', '中文定义', '发音', '英文定义', '词性分类']
    selected_post = {}
    post_data = {
        'word_list': [],
        'word_dict': {}
    }
    behavior_dict = {}

    @classmethod
    def init_data(cls):
        cls.selected_post = {}
        cls.post_data = {
            'word_list': [],
            'word_dict': {}
        }
        cls.behavior_dict = {}

    @classmethod
    def set_selected_post(cls, post_id=0, title="", url=""):
        # 所有文章列表
        cls.selected_post = {
            'post_id': post_id,
            'title': title,
            'url': url
        }
        return cls.selected_post

    @classmethod
    def create_post_words_full(cls, txt_post=""):
        # 选中文章对应单词列表(全)
        if not txt_post:
            cls.post_data['word_list'] = DbInterface(
            ).get_post_word_data(cls.selected_post['post_id'])
        else:
            cls.post_data['word_list'] = Views().get_post_words(txt_post)
        # 单词本内容
        word_type_dict = Views().get_word_type_dict(cls.post_data['word_list'])
        star_words_dict = DbInterface().get_words_detail(
            cls.post_data['word_list'])
        cls.post_data['word_dict'] = {}
        for word in cls.post_data['word_list']:
            detail = star_words_dict.get(str(word).lower(), {})
            cls.post_data['word_dict'][word] = {
                'translation': detail.get('translation', ''),
                'phonetic': detail.get('phonetic', ''),
                'definition': detail.get('definition', ''),
                'word_type': word_type_dict.get(str(word), ''),
            }
        return cls.selected_post.get('post_id', 0)

    @classmethod
    def init_behavior_dict(cls):
        # 0: 未读 1：已读 2：停用
        cls.behavior_dict = DbInterface().get_words_behavior(cls.post_data['word_list'])
        for word in cls.post_data['word_list']:
            if word in cls.behavior_dict:
                continue
            statu = 0
            if not(
                cls.post_data['word_dict'][word]['translation'] or
                cls.post_data['word_dict'][word]['definition']
            ):
                # 单词无定义，视为可停用
                statu = 2
            cls.behavior_dict[word] = statu
        return cls.behavior_dict

    @classmethod
    def get_word_list_shown(cls, words):
        word_list = []
        # word_list_header = ['单词', '中文定义', '发音', '英文定义', '词性分类']
        for word in words:
            word_list.append([
                word,
                cls.post_data['word_dict'][word]['translation'],
                cls.post_data['word_dict'][word]['phonetic'],
                cls.post_data['word_dict'][word]['definition'],
                settings.NLTK_WORD_TYPE_DICT.get(
                    cls.post_data['word_dict'][word]['word_type'], ''),
            ])
        return word_list
