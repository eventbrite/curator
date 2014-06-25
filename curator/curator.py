from jinja2 import Environment

from .loader import (
    LuaPackageLoader,
    PathComponent,
)


class Curator(object):

    redis = None
    env = None

    def __init__(self, package, scripts_dir, redis_client):
        self.env = Environment(
            loader=LuaPackageLoader(package, scripts_dir),
        )
        self.redis = redis_client
        self.cache = {}

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return PathComponent(self.env, self.redis, self.cache, attr)
