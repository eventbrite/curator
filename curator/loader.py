import hashlib
import os

from jinja2.exceptions import TemplateNotFound
from jinja2 import (
    Environment,
    PackageLoader,
)

# from wolverine import wolverine
# result = wolverine.util.mexists(['key1', 'key2'])

#class DottedPath(object):

    #def __getattribute__(self):


class ImproperlyConfigured(Exception):
    pass


class InvalidPath(Exception):
    pass


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


class LuaScript(object):

    def __init__(self, redis, template):
        self.redis = redis
        self.template = template

    def _get_template_sha(self):
        return hashlib.md5(self.template.get_source()).hexdigest()

    def __call__(self, *args, **kwargs):
        # TODO cache the rendered template
        import ipdb; ipdb.set_trace()
        template = self.template.render()
        print 'eval'


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
                return PathComponent(self.env, path)


class Curator(object):

    redis = None
    env = None

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            if self.redis is None:
                raise ImproperlyConfigured('Must call `set_redis_client`')

            if self.env is None:
                raise ImproperlyConfigured('Must call `configure_package`')

            return PathComponent(self.env, self.redis, attr)

    def configure_package(self, package, scripts_dir):
        self.env = Environment(
            loader=LuaPackageLoader(package, scripts_dir),
        )

    def set_redis_client(self, redis):
        self.redis = redis
