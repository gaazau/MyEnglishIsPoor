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

    def update_word_list(self, word_list, behavior_list):
        DbInterface().save_word_list(word_list)
        DbInterface().save_behavior(behavior_list)
        return True

    def delete_post_words(self, post_id):
        if not post_id:
            return True
        words = DbInterface().get_post_words_unique(post_id)
        DbInterface().delete_post(post_id)
        DbInterface().delete_post_words(post_id)
        if words:
            DbInterface().delete_behavior(words)
            DbInterface().delete_word_list(words)
        return True

    def get_post_words(self, txt_post):
        return self.extract_english_words(txt_post)


class GlobalData():
    word_list_header = ['单词', '中文定义', '发音', '英文定义', '词性分类']
    selected_post = {}
    post_data = {
        'word_list': [],
        'word_dict': {}
    }
    behavior_dict = {}
    words_filter_mode = 0 

    @classmethod
    def reset_data(cls):
        cls.selected_post = {
            "post_id": 0,
            "title": '',
            "url": '',
        }
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
    def get_post_words(cls, txt_post=""):
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
                'word': word,
                'translation': detail.get('translation', ''),
                'phonetic': detail.get('phonetic', ''),
                'definition': detail.get('definition', ''),
                'word_type': word_type_dict.get(str(word), ''),
            }
        return cls.post_data['word_list']

    @classmethod
    def init_behavior_dict(cls):
        # 0: 未读 1：已读 2：停用
        cls.behavior_dict = DbInterface().get_words_behavior(
            cls.post_data['word_list'])
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

    @classmethod
    def word_list_to_db(cls):
        return [v for v in cls.post_data['word_dict'].values()]

    @classmethod
    def behavior_list_to_db(cls):
        behavior_list = []
        for k, v in cls.behavior_dict.items():
            behavior_list.append({
                'word': k,
                'word_statu': v
            })
        return behavior_list

    # @classmethod
    # def post_dict_to_db(cls):
    #     return cls.selected_post

    @classmethod
    def post_words_to_db(cls):
        post_words = []
        if cls.selected_post['post_id']:
            for word in cls.post_data['word_list']:
                post_words.append({
                    'post_id': cls.selected_post['post_id'],
                    'word': word
                })
        return post_words
