from skr import rest_api
from skr.common import util
from skr.api.base import BaseAPI


@rest_api.route('/api/v1/ping', endpoint='ping')
class PingAPI(BaseAPI):

    def get(self):
        return util.api_response(data={
            'app_name': 'skr',
            'app_version': '1.0'
        })
