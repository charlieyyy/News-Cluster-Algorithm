import datetime
import dateparser

from skr.model.article import Article
from skr.common import algorithm
from skr.model.cluster import Cluster


class ClusterService():
    def __init__(self, time_range=None):
        """
        ClusterService init

        @param time_range: 需要聚类的日期，格式为'2018-08-22'
        @type time_range: str of day
        @return: None
        @rtype: None
        """

        if not time_range:
            self.time_range = str(datetime.date.today())
        else:
            self.time_range = time_range
            self.base_list = []

    def get_day_news(self):
        """
        得到当天的news，存入data

        @return: None
        @rtype: None
        """
        start_time = dateparser.parse(self.time_range)
        end_time_str = f'{self.time_range} 23:59:59'
        end_time = dateparser.parse(end_time_str)

        # 如果 self.time_range 是 2018-08-22，那么实际查询的是美国洛杉矶
        # `2018-08-21 05:00` ~ `2018-08-22 05:00`（美西，UTC-8）
        start_time = start_time + datetime.timedelta(hours=-3)
        end_time = end_time + datetime.timedelta(hours=-3)

        query = {'date__gte': start_time, 'date__lte': end_time}
        article_list = Article.objects(**query)
        data = list(article_list)
        data = [{'title': d['title'], 'content': d['content'],
                 'source': d['source'], 'url': d['url'], 'date': d['date']}
                for d in data]
        return data

    def run_cluster(self):
        """
        跑算法，存入算法返回的row_data（原始数据）, top_cluster（聚类结果),
        X(fidf vector）, features（关键词）

        @return: None
        @rtype: None
        """
        data = self.get_day_news()
        return algorithm.get_cluster_news(data)

    def save_to_db(self):
        """
        把聚类结构存入数据库

        @return: None
        @rtype: None
        """
        row_data, top_cluster, X, features = self.run_cluster()
        for topic in top_cluster:
            base_index = topic[0]
            base_title = row_data[base_index]['title']
            base_url = row_data[base_index]['url']
            base_source = row_data[base_index]['source']
            base_date = row_data[base_index]['date']
            base_content = row_data[base_index]['content']
            cluster = Cluster.get_by_topic_url(base_url)
            # day_ = base_date.strftime('%Y%m%d')
            day_ = dateparser.parse(self.time_range).strftime('%Y%m%d')
            if not cluster:
                cluster = Cluster(topic={'title': base_title,
                                         'url': base_url,
                                         'source': base_source,
                                         'source_cn': base_source,
                                         'date': base_date
                                         })
                cluster.summary = ''
                cluster.content = base_content
                cluster.type = 'Day'
                cluster.parent_id = day_
                cluster.tag = []
            news_list = []
            for item in topic:
                titles = row_data[item]['title']
                url = row_data[item]['url']
                source = row_data[item]['source']
                date = row_data[item]['date']
                news = {
                    'title': titles,
                    'url': url,
                    'source': source,
                    'source_cn': source,
                    'date': date
                }
                news_list.append(news)
            cluster.news = news_list
            cluster.news_count = len(topic)
            cluster.added = datetime.datetime.now()
            cluster.save()


def save_cluster_data():
    """
    保存当日聚类数据到数据库

    @return: None
    @rtype: None
    """
    service = ClusterService()
    service.save_to_db()


if __name__ == '__main__':
    import mongoengine
    mongoengine.connect('skr', host='localhost')
    save_cluster_data()
