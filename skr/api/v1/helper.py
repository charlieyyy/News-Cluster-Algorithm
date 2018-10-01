import datetime
import dateparser

from flask import request
from werkzeug.exceptions import BadRequest

from skr import rest_api
from skr.common import util
from skr.api.base import BaseAPI
from skr.service.email import send_geeks_read_email


@rest_api.route('/api/v1/helper/sendmail', endpoint='sendmail')
class SendMailAPI(BaseAPI):
    def post(self):
        """
        @api {post} /helper/sendmail 手动调度某些发邮件任务
        @apiName Helper
        @apiDescription 手动调度某些发邮件任务
        @apiVersion 1.0.0

        @apiParam {String} [command] 任务
        @apiParam {String} [date] 日期
        @apiParam {Array} [email] 邮件
        @apiParamExample {json} Request-Example:
        HTTP/1.1 200 SUCCESS
        {
            "msg": "SUCCESS"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 500 ERROR
        {
            "msg": "Something happend"
        }
        """
        data = request.get_json()
        command = data.get('command', None)
        day = data.get('date', None)
        email = data.get('email', None)

        if day is None:
            date_ = dateparser.parse(str(datetime.datetime.now()))
            day = str(date_.year) + str(date_.month) + str(date_.day)

        if command == 'daily':
            data = send_geeks_read_email(day, email)
            return util.api_response(data=data)
        else:
            raise BadRequest('Invalid command.')
