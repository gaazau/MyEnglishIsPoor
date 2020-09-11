# 将单词本上传至不背单词
import requests
from copy import deepcopy
import json

HEADER_NORMAL = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "bbdc.cn",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
}

MY_COOKIES = ""

def login_bbdc(user_id, password):
    global MY_COOKIES
    url_login = "https://bbdc.cn/login"
    params = {
        "userName": user_id,
        "passwd": password,
    }
    headers = deepcopy(HEADER_NORMAL)
    resp = requests.get(url_login, params=params, headers=HEADER_NORMAL)
    if json.loads(resp.content.decode())["result_code"] != 200:
        raise ValueError("登录失败")
    cookies = resp.cookies
    MY_COOKIES = requests.utils.dict_from_cookiejar(cookies)
    return True


def get_my_list():
    if not MY_COOKIES:
        raise ValueError("No cookie")
    url = "https://bbdc.cn/lexis/book/list"
    resp = requests.get(url=url, headers=HEADER_NORMAL, cookies=MY_COOKIES)
    return json.loads(resp.content.decode())


def post_my_list(words, name="normal", desc="normal"):
    if not MY_COOKIES:
        raise ValueError("No cookie")
    url_upload = "https://bbdc.cn/lexis/book/save"
    data = {
        "wordList": words,
        "name": name,
        "desc": desc
    }
    post_header = {
        **HEADER_NORMAL,
        "Origin": "https://bbdc.cn",
        "Referer": "https://bbdc.cn/lexis_book_index",
        "X-Requested-With": "XMLHttpRequest"
    }
    resp = requests.post(url_upload, data=data,
                         headers=post_header, cookies=MY_COOKIES)
    if json.loads(resp.content.decode())["result_code"] != 200:
        raise ValueError("提交单词本失败")
    return True
