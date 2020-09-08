import re
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
    