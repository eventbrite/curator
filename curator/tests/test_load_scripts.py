import unittest2

from curator import Curator
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

    def test_load_lua_include_partial(self):
        result = self.curator.util.include()
        self.assertEqual(result, 1)
