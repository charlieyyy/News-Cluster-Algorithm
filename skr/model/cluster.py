import mongoengine
import json

from skr.common import util
from skr.model.base_model import BaseModel


class Cluster(BaseModel, mongoengine.Document):
    topic = mongoengine.DictField(unique=True)
    news = mongoengine.ListField()
    news_count = mongoengine.IntField()
    parent_id = mongoengine.StringField()
    type = mongoengine.StringField()
    added = mongoengine.DateTimeField()
    summary = mongoengine.StringField()
    tags = mongoengine.ListField(default=[])
    content = mongoengine.StringField()

    meta = {
        'collection': 'clusters',
        'indexes': [
            'news_count',
            'parent_id',
            'type',
            {
                'fields': ['topic.url'],
                'unique': True
            },
            {
                'fields': ['parent_id', 'type']
            }
        ]
    }

    @classmethod
    def get_by_cluster_id(cls, id):
        return cls.objects(id=id).first()

    @classmethod
    def delete_by_cluster_id(cls, id):
        lunch = cls.objects(id=id).first()
        lunch.delete()

    @classmethod
    def get_by_topic_url(cls, url):
        return cls.objects(topic__url=url).first()

    @classmethod
    def get_day_news(cls, day_str=None) -> list:
        if day_str is None:
            day_str = util.get_last_day_str()

        query = {'parent_id': day_str}

        return cls.objects(**query).order_by('-news_count')

    @classmethod
    def get_day_news_top20(cls, day_str=None) -> list:
        if day_str is None:
            day_str = util.get_last_day_str()

        query = {'parent_id': day_str}

        return cls.objects(**query).order_by('-news_count').limit(20)

    def api_response(self):
        res = self.api_base_response()
        res['content'] = self.content
        return res

    def api_base_response(self):
        item = json.loads(self.to_json())
        item = util.item_pop(item, ['_id', 'content'])
        item['_id'] = str(self.id)
        return item
