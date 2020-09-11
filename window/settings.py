# 翻译中带有的内容视为停用词
STOP_WORDS_IN_TRANSLATION = [
    '人名',
    '地名'
]

# 直接停用词
STOP_WORDS_LIST = (*[chr(i) for i in range(65, 91)], *[chr(i) for i in range(97, 123)])
