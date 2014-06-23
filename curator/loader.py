import os

from jinja2.exceptions import TemplateNotFound
from jinja2 import PackageLoader

from .script import LuaScript


class LuaPackageLoader(PackageLoader):

    def get_source(self, environment, template):
        try:
            return super(LuaPackageLoader, self).get_source(
                environment,
                template,
            )
        except TemplateNotFound:
            if not template.endswith('.lua'):
                return super(LuaPackageLoader, self).get_source(
                    environment,
                    template + '.lua',
                )


class PathComponent(object):

    def __init__(self, env, redis, path):
        self.env = env
        self.path = path
        self.redis = redis

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            path = os.path.join(self.path, attr)
            try:
                return LuaScript(self.redis, self.env.get_template(path))
            except IOError:
                return PathComponent(self.env, self.redis, path)
