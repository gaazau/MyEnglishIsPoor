import re

class Views(object):
    def extract_english_words(self, content):
        """提取英文单词"""
        if not content:
            return []
        return sorted(set(re.findall(re.compile(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)*"), content)))