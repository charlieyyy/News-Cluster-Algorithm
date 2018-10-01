import json
import datetime
from nose import tools
from copy import deepcopy

from tests import test_app, skr_article, tech_article, tesla_article

from skr.model import Article
from skr.service.health_clean import clean_article


class TestArticle():
    @classmethod
    def setup_class(self):
        self.skr_article_data = deepcopy(skr_article)
        self.tech_article_data = deepcopy(tech_article)
        self.tesla_article_data = deepcopy(tesla_article)
        self.article_url_list = []
        self.__test_save_article()

    @classmethod
    def teardown_class(self):
        for url in self.article_url_list:
            articles = Article.objects(url=url).first()
            if articles:
                articles.delete()

    @classmethod
    def __test_save_article(self):
        data = json.dumps(self.skr_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        json_resp = json.loads(response.data)
        tools.assert_equals(response.status_code, 200)
        tools.assert_is_not_none(json_resp.get('data'))
        tools.assert_is_not_none(json_resp.get('data').get('source'))
        self.article_url_list.append(self.skr_article_data['url'])

    def test_article_post(self):
        """
        测试article的post接口

        """
        response = test_app.post('/api/v1/article')
        tools.assert_equals(response.status_code, 400)
        data = json.dumps(self.tech_article_data)

        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        self.article_url_list.append(self.tech_article_data['url'])

        json_resp = json.loads(response.data)
        tools.assert_equals(response.status_code, 200)
        tools.assert_is_not_none(json_resp.get('data'))
        tools.assert_is_not_none(json_resp.get('data').get('source'))

    def test_article_clean(self):
        """
        测试article自动清理功能
        """
        tesla_article_data = deepcopy(self.tesla_article_data)
        today = datetime.date.today()
        weekday = today.weekday()
        start_delta = datetime.timedelta(days=weekday, weeks=1)
        start_of_week = today - start_delta

        query = {'added__lte': start_of_week}
        articles = Article.objects(**query)
        tools.assert_equals(len(articles), 1)
        clean_article()
        articles = Article.objects(**query)
        tools.assert_equals(len(articles), 0)

        tesla_article_data['added'] = start_of_week
        tesla_article_data['date'] = start_of_week
        tesla_article_data['source'] = tesla_article_data['type']
        del tesla_article_data['type']
        del tesla_article_data['id']
        Article(**tesla_article_data).save()

        articles = Article.objects(**query)
        tools.assert_equals(len(articles), 1)
        clean_article()
        articles = Article.objects(**query)
        tools.assert_equals(len(articles), 0)
