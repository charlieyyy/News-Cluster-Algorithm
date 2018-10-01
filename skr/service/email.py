import copy
import asyncio

from skr import settings
from skr.common import util
from skr.model.cluster import Cluster
from skr.common.constant import GeeksReadEmail


class DailyNewsService(object):

    def __init__(self,
                 time_range=None,
                 receiver_email=None):
        """
        DailyNewsService初始方法

        @param time_range: 查询的日期,格式为:20180910
        @type time_range: str
        @receiver_email: 收件人邮箱地址,默认为
        @type: str of email address
        @return: None
        @rtype: None
        """
        if time_range is None:
            time_range = util.get_last_day_str()

        topic_news = Cluster.get_day_news_top20(day_str=time_range)
        if receiver_email is None:
            self.receiver_email = settings.DEFAULT_MAIL_LIST
        else:
            self.receiver_email = receiver_email

        self.subject = util.mail_generator(GeeksReadEmail.SUBJECT,
                                           {'time_range': time_range})
        news_content = (self.get_topics_news_content(
            topic_news=topic_news)
        )
        self.format_map = {
            'subject': self.subject,
            'news_content': news_content,
            'unsubscribe_link': '',
            'time_range': time_range
        }

    def send_news(self):
        """
        发送邮件

        @return: 发送邮件的结果列表
        @rtype: list of mail response
        """
        format_map = copy.deepcopy(self.format_map)
        # cancel_link = f'{settings.SUBSCRIBEURL}/cancel/{item.id}'
        format_map['unsubscribe_link'] = ''  # cancel_link
        email_content = util.mail_generator(GeeksReadEmail.EMAIL_TEMPLATE,
                                            format_map)
        tasks = [util.sendmail(self.subject, email_content, email)
                 for email in self.receiver_email]
        loop = asyncio.new_event_loop()
        done, pending = loop.run_until_complete(asyncio.wait(tasks, loop=loop))
        loop.close()
        return list(map(lambda x: x.result(), done))

    def get_topics_news_content(self, topic_news):
        """
        得到聚类topic的文章内容

        @param topic_news: 聚类出来的新闻
        @type topic_news: list of Cluster
        @return: 邮件正文
        @rtype: str
        """
        def get_topics_email_list(news):
            format_map = {'topic': news.topic['title'],
                          'topic_url': news.topic['url'],
                          'news_count': news.news_count,
                          'news_list': '',
                          'summary': news.summary}

            news_list = []
            for article in news.news:
                news_list.append(util.mail_generator(
                    GeeksReadEmail.NEWS_LIST, article))

            format_map['news_list'] = ''.join(news_list)
            return util.mail_generator(template=GeeksReadEmail.NEWS_CONTENT,
                                       format_map=format_map)

        content_list = []
        for item in topic_news:
            news_warp = get_topics_email_list(item)
            content_list.append(news_warp)

        topic_content = ''.join(content_list)
        return topic_content


def send_geeks_read_email(time_range=None, receiver_email=None):
    '''
    根据日期发送聚类邮件

    @param time_range: 查询的日期,格式为:20180910
    @type time_range: str
    @receiver_email: 收件人邮箱地址
    @type: str of email address
    @return: None
    @rtype: None
    '''
    service = DailyNewsService(time_range, receiver_email)
    return service.send_news()


if __name__ == '__main__':
    import mongoengine
    mongoengine.connect('skr', host='localhost')
    print(send_geeks_read_email())
