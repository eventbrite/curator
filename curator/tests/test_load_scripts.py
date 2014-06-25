import unittest2

from curator import Curator
from curator.loader import ScriptNotFound
from jinja2 import Template
import mock
from redis import Redis


TEST_DB = 10


class ScriptLoadingTests(unittest2.TestCase):

    def setUp(self):
        self.redis = Redis(db=TEST_DB)
        existing_keys = self.redis.keys('*')
        self.assertFalse(
            existing_keys,
            'Redis database "%s" must be empty to run these tests' % (TEST_DB,)
        )
        self.curator = Curator('curator', 'tests/sample_lua', self.redis)

    def tearDown(self):
        self.redis.flushdb()
        self.redis.script_flush()

    def test_load_mexists(self):
        result = self.curator.util.exists.mexists(
            keys=['key0', 'key2', 'key3'],
        )
        self.assertEqual(result, [0, 0, 0])

    def test_util_mexists(self):
        self.redis.set('key1', 'value')
        result = self.curator.util.exists.mexists(
            keys=['key0', 'key1', 'key2'],
        )
        self.assertEqual(result, [0, 1, 0])

    def test_load_lua_include_partial(self):
        result = self.curator.util.include()
        self.assertEqual(result, 1)

    def test_load_mexists_from_cache(self):
        # calling it the first time should put it in the cache
        result = self.curator.util.exists.mexists(keys=['key0', 'key1'])
        with mock.patch.object(Template, 'render') as mock_render:
            mock_render.return_value = 'test'
            cached_result = self.curator.util.exists.mexists(
                keys=['key0', 'key1'],
            )
            self.assertEqual(result, cached_result)
            # render should not have been called since we fetched from cache
            self.assertEqual(mock_render.call_count, 0)

    def test_access_nonexistant_script(self):
        with self.assertRaises(ScriptNotFound) as e:
            self.curator.invalid.path.to.script(keys=['key1'])
        self.assertEqual(e.exception.path, 'invalid/path/to/script')

    def test_load_script_base_dir(self):
        result = self.curator.base()
        self.assertEqual(result, 1)
