import json
import datetime
from copy import deepcopy
from nose import tools

from tests import test_app, skr_article, tech_article, tesla_article
from tests import test_content, compare_content, test_title, compare_title

from skr.model import Article, Cluster
from skr.service.cluster import ClusterService
from skr.service.health_clean import clean_cluster


class TestCluster():
    @classmethod
    def setup_class(self):
        self.skr_article_data = deepcopy(skr_article)
        self.tech_article_data = deepcopy(tech_article)
        self.tesla_article_data = deepcopy(tesla_article)
        self.article_url_list = []
        self.__test_save_article()
        self.__test_save_early_article()

    @classmethod
    def teardown_class(self):
        for url in self.article_url_list:
            articles = Article.objects(url=url).first()
            if articles:
                articles.delete()

    @classmethod
    def __test_save_article(self):
        self.skr_article_data['title'] = compare_title
        self.skr_article_data['content'] = compare_content
        data = json.dumps(self.skr_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        json_resp = json.loads(response.data)
        tools.assert_equals(response.status_code, 200)
        tools.assert_is_not_none(json_resp.get('data'))
        tools.assert_is_not_none(json_resp.get('data').get('source'))

        self.tech_article_data['title'] = test_title
        self.tech_article_data['content'] = test_content
        data = json.dumps(self.tech_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        self.tesla_article_data['title'] = test_title
        self.tesla_article_data['content'] = test_content
        data = json.dumps(self.tesla_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        self.article_url_list.append(self.skr_article_data['url'])
        self.article_url_list.append(self.tech_article_data['url'])
        self.article_url_list.append(self.tesla_article_data['url'])

    @classmethod
    def __test_save_early_article(self):
        """
        ClusterService 中 query 的时间段是 昨天21:00 ~ 当天21:00，
        设置原始数据时间为 2018-08-14 21:00:00，新增三篇 2018-08-14 20:59:59 文章，
        不应该影响 `test_cluster_get` 测试的结果
        """
        skr_article_data = deepcopy(self.skr_article_data)
        skr_article_data['title'] = compare_title
        skr_article_data['content'] = compare_content
        skr_article_data['url'] += '111'
        skr_article_data['date'] -= 1
        data = json.dumps(skr_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        json_resp = json.loads(response.data)
        tools.assert_equals(response.status_code, 200)
        tools.assert_is_not_none(json_resp.get('data'))
        tools.assert_is_not_none(json_resp.get('data').get('source'))

        tech_article_data = deepcopy(self.tech_article_data)
        tech_article_data['title'] = test_title
        tech_article_data['content'] = test_content
        tech_article_data['url'] += '222'
        tech_article_data['date'] -= 1
        data = json.dumps(tech_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        tesla_article_data = deepcopy(self.tesla_article_data)
        tesla_article_data['title'] = test_title
        tesla_article_data['content'] = test_content
        tesla_article_data['url'] += '333'
        tesla_article_data['date'] -= 1
        data = json.dumps(tesla_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        self.article_url_list.append(self.skr_article_data['url'])
        self.article_url_list.append(self.tech_article_data['url'])
        self.article_url_list.append(self.tesla_article_data['url'])

    def test_cluster_get(self):
        """
        测试cluster的get接口

        """

        service = ClusterService('2018/08/15')
        service.save_to_db()

        response = test_app.get('/api/v1/cluster?day=20180815')
        tools.assert_equals(response.status_code, 200)

        json_resp = json.loads(response.data)
        tools.assert_equals(response.status_code, 200)
        tools.assert_is_not_none(json_resp.get('data'))
        data = json_resp.get('data')
        tools.assert_equals(len(data), 2)
        news = data[0]['news']
        tools.assert_equals(data[0]['topic']['title'], news[0]['title'])
        tools.assert_equals(news[0]['title'], news[1]['title'])
        first_topic = data[0]['topic']['title']
        second_topic = data[1]['topic']['title']

        # test update cluster, topic unchanged
        self.skr_article_data['title'] = compare_title
        self.skr_article_data['content'] = compare_content
        self.skr_article_data['url'] = 'http://www.skr.net/yeah/'
        data = json.dumps(self.skr_article_data)
        response = test_app.post('/api/v1/article',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)

        service = ClusterService('2018/08/15')
        service.save_to_db()

        response = test_app.get('/api/v1/cluster?day=20180815')
        tools.assert_equals(response.status_code, 200)

        json_resp = json.loads(response.data)
        tools.assert_equals(response.status_code, 200)
        tools.assert_is_not_none(json_resp.get('data'))
        data = json_resp.get('data')
        tools.assert_equals(len(data), 2)

        tools.assert_equals(first_topic, data[0]['topic']['title'])
        tools.assert_equals(second_topic, data[1]['topic']['title'])

        news = data[0]['news']
        tools.assert_equals(data[0]['topic']['title'], news[0]['title'])
        tools.assert_equals(news[0]['title'], news[1]['title'])

        news = data[1]['news']
        tools.assert_equals(data[1]['topic']['title'], news[0]['title'])
        tools.assert_equals(news[0]['title'], news[1]['title'])

        # test length of cluster is correct
        news_count = data[0]['news_count']
        tools.assert_equals(news_count, 2)
        self.__test_send_mail()

    @tools.nottest
    def __test_send_mail(self):
        """
        测试邮件功能
        """
        data = dict(command='daily',
                    date='20180815',
                    email=['caihaoyu@geekpark.net', 'wuwenhan@geekpark.net']
                    )
        data = json.dumps(data)
        response = test_app.post('/api/v1/helper/sendmail',
                                 data=data,
                                 content_type='application/json')
        tools.assert_equals(response.status_code, 200)
        json_resp = json.loads(response.data).get('data')
        tools.assert_is_not_none(json_resp)
        tools.assert_equals(len(json_resp), 2)
        for result in json_resp:
            tools.assert_equals(result['status'], True)

    def test_cluster_clean(self):
        """
        测试cluster自动清理功能
        """
        today = datetime.date.today()
        weekday = today.weekday()
        start_delta = datetime.timedelta(days=weekday, weeks=1)
        start_of_week = today - start_delta

        test_cluster = {
            "topic": {
                "title": "US targets Chinese tech with a 25 percent tariff",
                "url": "https://www.engadget.com",
                "source": "engadget"
            },
            "news": [
                {
                    "title": "U.S. tariffs target Chinese...",
                    "url": "http://www.autonews.com",
                    "source": "autonews"
                },
                {
                    "title": "China fires back at Trump with tariffs",
                    "url": "http://www.businessinsider.com",
                    "source": "businessinsider"
                },
            ],
            "news_count": 11,
            "parent_id": '20180815',
            "type": 'yahoo',
            "added": start_of_week,
            "summary": 'blabla',
            "tags": [],
            "content": 'balala'
        }
        Cluster(**test_cluster).save()
        query = {'added__lte': start_of_week}
        clusters = Cluster.objects(**query)
        tools.assert_equals(len(clusters), 1)
        clean_cluster()
        clusters = Cluster.objects(**query)
        tools.assert_equals(len(clusters), 0)
