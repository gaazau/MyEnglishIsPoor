from app.behavior.view.modules import WorkerPost
from app.behavior.view.modules import WorkerWord
from app.behavior.view.modules import WorkerUser
from app.behavior.view.modules import DataWorker


class BehaviorViews(object):
    def __init__(self, user_id):
        self.user_id = user_id
    # 用户提供文章

    def get_words_from_post(self, file_path):
        """从文章中获取单词内容"""
        wp = WorkerPost()
        wp.work_for_user_id = self.user_id

        rows = wp.read_file_by_rows(file_path)
        words_set = set()
        for row in rows:
            origin_words = wp.extract_english_words(row, to_set=True)
            clean_words = wp.exclude_stop_words(origin_words)
            words_set.update(clean_words)
        return sorted(list(words_set))

    # 文章单词表
    def get_words_detail(self, words_list):
        ww = WorkerWord()
        ww.work_for_user_id = self.user_id
        detail_words, miss_words = ww.get_words_detail_info(words_list)
        return {"detail_words": sorted(detail_words, key=lambda x:x['word']), "miss_words": sorted(miss_words)}

    # 保存当前单词表
    def commit_words_list(self, words_list):
        wu = WorkerUser()
        wu.work_for_user_id = self.user_id
        wu.save_words_to_collect_dict(words_list)
        return True

    # # 获取单词列表
    # def get_words_list(self):
    #     wu = WorkerUser()
    #     wu.work_for_user_id = self.user_id
    #     reutrn wu.get_words_list()