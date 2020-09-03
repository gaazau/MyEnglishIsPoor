from app.behavior.view.views import BehaviorViews


class TestViews:
    def test_default(self):
        assert 1 == 1

    def test_get_words_from_post(self):
        bv = BehaviorViews(1001)
        words_list = bv.get_words_from_post("static/test_post.txt")
        # print(words_list)
        assert set(words_list) == set(['A', 'A-AA', 'AA', "Who's", 'a-aa', 'aa', 'book',
                                     'go', 'hello', 'o', 'od', 'ok', 'test', 'with', 'world'])
    
    def test_get_words_detail(self):
        bv = BehaviorViews(1001)
        words_list = bv.get_words_from_post("static/test_post.txt")
        word_package = bv.get_words_detail(words_list)
        assert len(words_list) == len(word_package['miss_words']) + len(word_package['detail_words'])

        assert word_package['miss_words'] == ['A-AA', 'a-aa']

        word_world = word_package['detail_words'][-1]
        for k,v in word_world.items():
            # print("%s:%s" % (k,v))
            assert k in ('word', 'phonetic', 'definition', 'translation','type', 'short_type', 'name')
            assert len(word_world[k]) > 0

    
    def test_commit_words_list(self):
        bv = BehaviorViews(1001)
        words_list = bv.get_words_from_post("static/test_post.txt")
        word_package = bv.get_words_detail(words_list)

        bv.commit_words_list(word_package['detail_words'])
    
    def test_get_user_dict(self):
        bv = BehaviorViews(1001)
        cur_words_list = bv.get_words_list()
        