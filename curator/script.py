import hashlib

from redis.exceptions import NoScriptError


class LuaScript(object):

    def __init__(self, redis, template):
        self.redis = redis
        self.template = template
        self.script = self._render_template(template)

    def _render_template(self, template):
        # TODO try and fetch this from the curator cache
        return template.render()

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
        except NoScriptError:
            response = self.redis.eval(self.script, num_keys, *keys_and_args)
        return response
