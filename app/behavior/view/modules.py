import re

from nltk import word_tokenize
from nltk import pos_tag

from app.behavior.data.interface import DBWorker
from app import settings


class WorkerPost():
    """提供文章

    1. 读取文章内容
    2. 解析文章内容获取特定规则的单词
    """

    def __init__(self):
        self.english_words_pattern = re.compile(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)*")
        self.stop_words = None
        self.work_for_user_id = 0

    def to_flush_content(self):
        if self.flush:
            self.flush = False
            return True
        return False

    def read_file_by_rows(self, file_path):
        """逐行读取本地文件内容"""
        with open(file_path, mode="r") as f:
            for row in f.readlines():
                yield row

    def extract_english_words(self, content, to_set=False):
        """提取英文单词"""
        if not content:
            return []
        if to_set:
            return set(re.findall(self.english_words_pattern, content))
        return list(re.findall(self.english_words_pattern, content))

    def exclude_stop_words(self, src_words_set):
        """排除停用词"""
        user_ids = set()
        if self.work_for_user_id:
            user_ids.add(self.work_for_user_id)
        if not user_ids:
            return src_words_set
        stop_words = set(DBWorker().get_stop_words(user_ids))
        return src_words_set - stop_words


class WorkerWord(object):
    """单词表操作"""

    def __init__(self):
        self.work_for_user_id = 0

    def get_word_type_dict(self, words_list):
        tokens = word_tokenize("\n".join(words_list))
        tags = pos_tag(tokens)
        tags_dict = {}
        for tag in tags:
            tags_dict[tag[0]] = {
                "type": tag[1],
                "short_type": tag[1][0],
                "name": settings.NLTK_WORD_TYPE_DICT.get(tag[1], "")
            }
        return tags_dict

    def get_words_detail_info(self, words_list):
        word_done_list = []
        word_miss_list = []
        if not words_list:
            return word_done_list, word_miss_list
        lower_word_list = [word.lower() for word in words_list]
        detail_dict = DBWorker().get_words_detail(lower_word_list)
        word_type_dict = self.get_word_type_dict(words_list)
        
        for word in words_list:
            if word.lower() not in detail_dict:
                word_miss_list.append(word)
                continue
            detail = detail_dict[word.lower()]
            word_done_list.append({
                "word": word,
                "phonetic": detail.phonetic,
                "definition": detail.definition,
                "translation": detail.translation,
                "type": word_type_dict.get(word, {}).get('type', ''),
                "short_type": word_type_dict.get(word, {}).get('short_type', ''),
                "name": word_type_dict.get(word, {}).get('name', ''),
            })
        return word_done_list, word_miss_list

    def filter_words_in_history_data(self, words_list, word_miss_list):
        words = [row['word'] for row in words_list]
        collect_words_set = set(DBWorker().get_words_in_history(
            self.work_for_user_id, words_list))
        new_words_list = []
        new_words_miss_list = []
        for words in words_list:
            if words['word'] in collect_words_set:
                continue
            new_words_list.append(words)

        for word in word_miss_list:
            if word in collect_words_set:
                continue
            new_words_miss_list.append(words)

        return new_words_list, new_words_miss_list


class DataWorker(object):
    """历史数据操作"""

    def __init__(self, user_id):
        self.work_for_user_id = user_id

    def get_history_data(self):
        words_list = []
        words_data = DBWorker().get_history_words(self.work_for_user_id)
        for row in words_data:
            words_list.append({
                "user_id": row["user_id"],
                "collect_dict_id": row["collect_dict_id"],
                "like": row["like"],
                "is_junk": row["is_junk"],
                "is_stop": row["is_stop"],
                "is_core": row["is_core"],
                "is_done": row["is_done"],
                "search_count": row["search_count"],
                "last_search_at": row["last_search_at"],
                "repeat_count": row["repeat_count"],
                "batch_id": row["batch_id"],
                "remark": row["remark"],
                "word": row["word"],
                "kind_id": row["kind_id"],
                "phonetic": row["phonetic"],
                "definition": row["definition"],
                "translation": row["translation"],
                "nltk_type_id": row["nltk_type_id"],
                "create_at": row["create_at"],
            })
        return words_list


class WorkerUser(object):
    """用户行为"""

    def __init__(self):
        self.work_for_user_id = 0

    def save_words_to_collect_dict(self, words_list):
        words = sorted({words['word'] for words in words_list})
        query = DBWorker().get_word_collection(words)
        exists_words = [row.word for row in query]
        need_to_save_words = []
        for row in words_list:
            if row['word'] in exists_words:
                continue
            need_to_save_words.append(row)
        DBWorker().insert_words_into_collect_dict(need_to_save_words)

        behavior_words = sorted({words['word'] for words in need_to_save_words})
        query = DBWorker().get_word_collection(behavior_words)
        need_to_save_bahavior = [row.id for row in query]
        DBWorker().insert_to_behavior(self.work_for_user_id, need_to_save_bahavior)
        return True
    
    def get_words_list(self):
        return  DBWorker().get_user_dict_record(self.work_for_user_id)