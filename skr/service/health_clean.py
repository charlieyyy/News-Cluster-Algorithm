import datetime

from skr.model.article import Article
from skr.model.cluster import Cluster


def clean_article():
    """
    删除一周前的article数据

    @return: None
    @rtype: None
    """
    today = datetime.date.today()
    weekday = today.weekday()
    start_delta = datetime.timedelta(days=weekday, weeks=1)
    start_of_week = today - start_delta
    query = {'added__lte': start_of_week}
    articles = Article.objects(**query)
    articles.delete()


def clean_cluster():
    """
    删除一周前的cluster数据

    @return: None
    @rtype: None
    """
    today = datetime.date.today()
    weekday = today.weekday()
    start_delta = datetime.timedelta(days=weekday, weeks=1)
    start_of_week = today - start_delta
    query = {'added__lte': start_of_week}
    clusters = Cluster.objects(**query)
    clusters.delete()


if __name__ == '__main__':
    import mongoengine
    mongoengine.connect('skr', host='localhost')
    clean_article()
