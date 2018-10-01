import datetime

from skr import rest_api
from skr.api.base import BaseAPI
from skr.model.cluster import Cluster
from skr.common import util

from flask_restful import reqparse

parser = reqparse.RequestParser()


@rest_api.route('/api/v1/cluster', endpoint='cluster')
@rest_api.route('/api/v1/cluster/<string:id>', endpoint='cluster_detail')
class ClusterAPI(BaseAPI):
    def get(self, id=None):
        """
        @api {get}} /cluster 文章聚类get接口
        @apiName clusterlist
        @apiGroup clusterlist
        @apiDescription 保存聚类结果到cluster数据库
        @apiVersion 1.0.0

        @apiParamExample {json} Response-Example:
        {
        "_id" : ObjectId("5b71436c384787e79f2064be"),
        "topic" : {
                "title" : "US targets Chinese tech with a 25 percent tariff",
                "url" : "https://www.engadget.com",
                "source" : "engadget"
        },
        "news" : [
                {
                        "title" : "U.S. tariffs target Chinese...",
                        "url" : "http://www.autonews.com",
                        "source" : "autonews"
                },
                {
                        "title" : "China fires back at Trump with tariffs",
                        "url" : "http://www.businessinsider.com",
                        "source" : "businessinsider"
                },
        "news_count" : 11,
        "parent_id": 20180815,
        "type": yahoo,
        "added":2018-08-15 00:00,
        "summary": blabla,
        "tags":[],
        "content": balala
        }
        """
        if not id:
            parser.add_argument('day', type=str, default='')
            args = parser.parse_args()
            date = args.get('day')
            if date:
                clusters = Cluster.objects(parent_id=date).order_by(
                    '-new_count')
                return util.api_response([c.api_base_response()
                                          for c in clusters])
            else:
                query_date = datetime.date.today()
                day_ = query_date.strftime('%Y%m%d')
                clusters = Cluster.objects(parent_id=day_).order_by(
                    '-new_count')
                return util.api_response([c.api_base_response()
                                          for c in clusters])
        else:
            cluster = Cluster.get_by_cluster_id(id)
            return util.api_response(cluster.api_response())
