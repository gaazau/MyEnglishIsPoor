import json 

with open("config.json", "r") as f:
    CONFIG = json.load(f)

# 翻译中带有的内容视为停用词
STOP_WORDS_IN_TRANSLATION = CONFIG['STOP_WORDS_IN_TRANSLATION']

# 直接停用词
STOP_WORDS_LIST = CONFIG['STOP_WORDS_LIST']


# sqlite db， 单词本及行为定义的相关库表
MY_WORDS_DB = CONFIG['MY_WORDS_DB']

# 不背单词的个人账号密码
BBDC_USER_NAME = CONFIG['BBDC_USER_NAME']
BBDC_PASSWORD = CONFIG['BBDC_PASSWORD']

# 筛选状态
FILTER_MODE = {
    0: "全部",
    1: "未读",
    2: "标记",
    3: "掌握",
    4: "停用",
    5: "非停用",
}