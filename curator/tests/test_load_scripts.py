import unittest

from curator import curator
from jinja2 import (
    Environment,
    PackageLoader,
)
from redis import Redis


TEST_DB = 10


class ScriptLoadingTests(unittest.TestCase):

    def setUp(self):
        self.redis = Redis(db=TEST_DB)
        existing_keys = self.redis.keys('*')
        self.assertFalse(
            existing_keys,
            'Redis database "%s" must be empty to run these tests' % (TEST_DB,)
        )
        curator.configure_package('curator', 'tests/sample_lua')
        curator.set_redis_client(self.redis)

    def tearDown(self):
        self.client.flushdb()

    def test_load_mexists(self):
        curator = Curator('curator', 'tests/sample_lua')
        result = curator.util.exists.mexists(['key0', 'key2', 'key3'])
        self.assertEqual(result, [0, 0, 0])
