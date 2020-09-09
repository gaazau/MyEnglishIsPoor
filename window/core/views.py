import re
import settings
from nltk import word_tokenize
from nltk import pos_tag

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
    
    def filter_done_words(self, word_list):
        done_words = DbInterface().get_done_word_list(word_list)
        return [word for word in word_list if word not in done_words]
    
    def save_word_list(self, word_list, behavior_list):
        word_data = []
        behavior_data = []
        stop_word_data = []
        for i, row in enumerate(word_list):
            if  0 <= behavior_list[i] < 2:
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
        return True