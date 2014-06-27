import hashlib

from redis.exceptions import ResponseError


class LuaScript(object):

    def __init__(self, redis, template, cache):
        self.redis = redis
        self.template = template
        self.cache = cache
        self.script = self._render_template(template)

    def _render_template(self, template):
        if template.filename in self.cache:
            script = self.cache[template.filename]
        else:
            script = template.render()
            self.cache[template.filename] = script
        return script

    def _get_script_sha(self):
        return hashlib.sha1(self.script).hexdigest()

    def __call__(self, *args, **kwargs):
        script_sha = self._get_script_sha()
        keys = kwargs.get('keys', [])
        arguments = kwargs.get('args', [])
        num_keys = len(keys)
        keys_and_args = keys + arguments
        try:
            response = self.redis.evalsha(script_sha, num_keys, *keys_and_args)
        except ResponseError:
            response = self.redis.eval(self.script, num_keys, *keys_and_args)
        return response
