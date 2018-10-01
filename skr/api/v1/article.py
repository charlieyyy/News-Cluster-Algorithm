import datetime

from flask import request

from skr import rest_api
from skr.common import util
from skr.model.article import Article
from skr.api.base import BaseAPI


@rest_api.route('/api/v1/article', endpoint='article')
class ArticleAPI(BaseAPI):

    def post(self):
        """
        @api {post}} /article 爬虫推送文章接口
        @apiName articlelist
        @apiGroup articlelist
        @apiDescription 保存文章到article数据库
        @apiVersion 1.0.0

        @apiParamExample {json} Request-Example:
        {
            "id":43718247,
            "title":"i am a good boy"
            "content":"you are a girl"
            "url":"hubb.net"
            "date":"20180819"
            "type": "wallstreet"
            "added": "2018-6-10 08:20"
        }
        """
        data = request.get_json(force=True)
        data['date'] = datetime.datetime.fromtimestamp(data['date'])
        data['added'] = datetime.datetime.fromtimestamp(data['added'])
        data['source'] = data['type']
        del data['type']
        del data['id']
        articles = Article(**data).save()

        if articles:
            return util.api_response(articles.api_response())
        else:
            raise ValueError('save failure')
