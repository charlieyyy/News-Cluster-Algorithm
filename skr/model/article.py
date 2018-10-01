import mongoengine
from skr.model.base_model import BaseModel


class Article(BaseModel, mongoengine.Document):
    title = mongoengine.StringField(required=True)
    content = mongoengine.StringField(required=True)
    url = mongoengine.URLField(required=True, unique=True)
    date = mongoengine.DateTimeField(required=True)
    source = mongoengine.StringField(required=True)
    added = mongoengine.DateTimeField(required=True)

    meta = {
        'collection': 'articles',
        'indexes': [
            {
                'fields': ['url'],
                'unique': True
            }
        ],
        'strict': False
    }

    @classmethod
    def get_by_url(cls, url):
        return cls.objects(url=url).first()

    @classmethod
    def delete_by_url(cls, url):
        lunch = cls.objects(url=url).first()
        lunch.delete()

    def api_base_response(self):
        return {'title': self.title, 'url': self.url, 'source': self.source}

    def api_response(self):
        return {
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'date': self.date.timestamp(),
            'source': self.source,
            'added': self.added.timestamp()
        }
