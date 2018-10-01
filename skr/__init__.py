from flask import Flask
import types
from skr.api.base import Process

app = Flask(__name__)


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper


rest_api = Process(app)

rest_api.route = types.MethodType(api_route, rest_api)
