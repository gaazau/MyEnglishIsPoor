import re
from copy import deepcopy

from core.db.db_interface import DbInterface
import settings


class Views(object):
    def extrace_re_content(self, re_pattern, content):
        if not content:
            return []
        pattern = re.compile(re_pattern)
        result = []
        for value in re.findall(pattern, content):
            if isinstance(value, tuple):
                result.append(" ".join(value))
            else:
                result.append(value)
        return result

    def extract_english_words(self, content):
        """提取英文单词"""
        if not content:
            return []
        return sorted(set(self.extrace_re_content(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)*", content)))

    def extract_english_phrase(self, content):
        """提取英文短语

        提取模式: A B 介 | A 介 | B 介 | B 介 C | 介 C D | 介 D |  介 C
        去重后返回
        """
        if not content:
            return []
        phrase_set = set()
        word = "([a-zA-Z]+)"
        prev = "(about|above|across|after|among|at|behind|below|besides|beside|between|by|except|for|from|front|inside|into|in|off|of|on|opposite|outside|over|throughout|through|to|under|without|within|with)"
        # 保证是介词，而不是某个单词中的截断内容
        no_alph_behind = "(?![a-zA-Z])"
        no_alph_before = "(?<![a-zA-Z])"
        # A B 介
        re_pattern = r"" + word + " " + word + " " + prev + no_alph_behind
        result = set(
            self.extrace_re_content(
                re_pattern,
                content,
            )
        )
        phrase_set.update(result)
        # A 介
        for p in result:
            words = p.split()
            phrase_set.add(words[0] + " " + words[2])
        # B 介
        re_pattern = r"" + word + " " + prev + no_alph_behind
        result = set(
            self.extrace_re_content(
                re_pattern,
                content,
            )
        )
        phrase_set.update(result)
        # B 介 C
        re_pattern = r"" + word + " " + prev + " " + word
        result = set(
            self.extrace_re_content(
                re_pattern,
                content,
            )
        )
        phrase_set.update(result)
        # 介 C
        re_pattern = r""+ no_alph_before + prev + " " + word
        result = set(
            self.extrace_re_content(
                re_pattern,
                content,
            )
        )
        phrase_set.update(result)
        # 介 C D
        re_pattern = r""+ no_alph_before + prev + " " + word + " " + word
        result = set(
            self.extrace_re_content(
                re_pattern,
                content,
            )
        )
        phrase_set.update(result)
        # 介 D
        for p in result:
            words = p.split()
            phrase_set.add(words[0] + " " + words[2])
        return sorted([str(w).lower() for w in phrase_set])

    def exclude_stop_words(self, src_words, stop_words):
        if not stop_words or not src_words:
            return src_words
        new_words = []
        for word in src_words:
            if word in stop_words:
                continue
            new_words.append(word)
        return new_words

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

    current_words = []

    @ classmethod
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
        cls.current_words = []

    @classmethod
    def set_selected_post(cls, post_id=0, title="", url=""):
        # 所有文章列表
        cls.selected_post = {
            'post_id': post_id,
            'title': title,
            'url': url
        }
        return cls.selected_post

    @staticmethod
    def exlude_bad_words(origin_words):
        clean_words = set()
        # 全部转换为小写
        for word in origin_words:
            clean_words.add(str(word).lower())
        return sorted(clean_words)

    @classmethod
    def get_post_words(cls, txt_post=""):
        # 选中文章对应单词列表(全)
        if not txt_post:
            origin_words = DbInterface(
            ).get_post_word_data(cls.selected_post['post_id'])
        else:
            origin_words = Views().get_post_words(txt_post)
        # 单词本内容
        star_words_dict = DbInterface().get_words_detail(origin_words)
        cls.post_data['word_list'] = cls.exlude_bad_words(origin_words)
        cls.post_data['word_dict'] = {}
        for word in cls.post_data['word_list']:
            detail = star_words_dict.get(str(word).lower(), {})
            cls.post_data['word_dict'][word] = {
                'word': word,
                'translation': detail.get('translation') or '--',
                'phonetic': detail.get('phonetic') or '--',
                'definition': detail.get('definition') or '--',
                'pos': detail.get('pos') or '--',
            }

        # 解析短语
        origin_phrase_list = Views().extract_english_phrase(txt_post)
        phrase_dict = DbInterface().get_words_detail(origin_phrase_list)
        for phrase in origin_phrase_list:
            detail = phrase_dict.get(phrase, {})
            if not detail:
                continue
            if not (detail["translation"] or detail["definition"]):
                continue
            cls.post_data['word_dict'][phrase] = {
                'word': phrase,
                'translation': detail.get('translation') or '--',
                'phonetic': detail.get('phonetic') or '--',
                'definition': detail.get('definition') or '--',
                'pos': 'zz',
            }
            cls.post_data['word_list'].append(phrase)
        return cls.post_data['word_list']

    @staticmethod
    def is_stop_words(word_obj):
        if not (word_obj['translation'] or word_obj['definition']):
            # 无释义
            return True
        if word_obj['word'] in settings.STOP_WORDS_LIST:
            return True
        if "'" in word_obj['word']:
            return True
        for stop_word in settings.STOP_WORDS_IN_TRANSLATION:
            if stop_word in word_obj['translation']:
                return True
        return False

    @classmethod
    def init_behavior_dict(cls):
        # 0: 未读 1：标记 2：掌握 3: 停用
        cls.behavior_dict = DbInterface().get_words_behavior(
            cls.post_data['word_list'])
        for word in cls.post_data['word_list']:
            if word in cls.behavior_dict:
                continue
            statu = 0
            if cls.is_stop_words(cls.post_data['word_dict'][word]):
                # 可停用词
                statu = 3
            cls.behavior_dict[word] = statu
        return cls.behavior_dict

    @staticmethod
    def get_frequent_word_type(pos):
        """选取最常用的词性作为分类"""
        pos_list = pos.split("/")
        try:
            if len(pos_list) <= 1:
                return pos.split(":")[0]
            new_post_list = [pos.split(":") for pos in pos_list]
            return sorted(new_post_list, key=lambda x: x[1], reverse=True)[0][0]
        except Exception:
            return "-"

    @classmethod
    def get_word_list_shown(cls, words):
        word_list = []
        # word_list_header = ['单词', '中文定义', '发音', '英文定义', '词性分类']
        for word in words:
            word_type_frequent = cls.get_frequent_word_type(
                cls.post_data['word_dict'][word]['pos'])
            word_list.append([
                word,
                cls.post_data['word_dict'][word]['translation'],
                cls.post_data['word_dict'][word]['phonetic'],
                cls.post_data['word_dict'][word]['definition'],
                word_type_frequent
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
