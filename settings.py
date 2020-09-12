# 翻译中带有的内容视为停用词
STOP_WORDS_IN_TRANSLATION = [
    '人名',
    '地名'
]

# 直接停用词
STOP_WORDS_LIST = (
    *[chr(i) for i in range(65, 91)],
    *[chr(i) for i in range(97, 123)],
    *['a', 'any word to stop']
)

# 筛选状态
FILTER_MODE = {
    0: "全部",
    1: "未读",
    2: "标记",
    3: "掌握",
    4: "停用",
    5: "非停用",
}

# sqlite db， 单词本及行为定义的相关库表
MY_WORDS_DB = "my_words.db"