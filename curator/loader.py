import os

from jinja2.exceptions import TemplateNotFound
from jinja2 import PackageLoader

from .script import LuaScript


class ScriptNotFound(Exception):
    """Exception raised when trying to use a script that doesn't exist"""

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path', None)
        super(ScriptNotFound, self).__init__(*args, **kwargs)


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

    def __init__(self, env, redis, cache, path):
        self._env = env
        self._path = path
        self._redis = redis
        self._cache = cache

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            path = os.path.join(self._path, attr)
            try:
                return LuaScript(
                    self._redis,
                    self._env.get_template(path),
                    self._cache,
                )
            except IOError:
                return PathComponent(self._env, self._redis, self._cache, path)

    def __call__(self, *args, **kwargs):
        raise ScriptNotFound('No lua script found at path', path=self._path)
