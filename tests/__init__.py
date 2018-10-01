import mongoengine

from skr import app

test_app = app.test_client()

mongoengine.connect('mongoenginetest', host='mongomock://localhost')


skr_article = {"id": 437182472,
               "title": "skr show has a bad start",
               "content": "skr wu gg si mi da",
               "url": "http://www.skr.net/1",
               "date": 1534251600,
               "type": "wallstreet",
               "added": 1534282080
               }

tech_article = {"id": 437182473,
                "title": "Elon Musk Plans to Take Tesla Private",
                "content": "Elon musk said on monday, he is planning to",
                "url": "http://www.wallstreet",
                "date": 1534251600,
                "type": "wallstreet",
                "added": 1534282080
                }

tesla_article = {"id": 437182474,
                 "title": "tesla may become private company",
                 "content": "elon musk said on monday that he is planning to",
                 "url": "http://www.skr.net",
                 "date": 1534251600,
                 "type": "wallstreet",
                 "added": 1534282080
                 }

compare_content_file = open('./tests/constant/compare_content.txt', 'r')
compare_content = compare_content_file.read().strip()
compare_content_file.close()

compare_title_file = open('./tests/constant/compare_title.txt', 'r')
compare_title = compare_title_file.read().strip()
compare_title_file.close()

test_content_file = open('./tests/constant/test_content.txt', 'r')
test_content = test_content_file.read().strip()
test_content_file.close()

test_title_file = open('./tests/constant/test_title.txt', 'r')
test_title = test_title_file.read().strip()
test_title_file.close()
