import unittest

from src.utils.api.cache import cache, clear_all_cached, clear_cache
from src.utils.api.types import Params


class DummyResponse:
    def __init__(self):
        self.headers = {}


class TestCache(unittest.TestCase):
    # flush cache to ensure no colisions between tests
    def tearDown(self):
        clear_all_cached()

    def test_cache_hit_and_miss(self):
        calls = 0

        @cache(expire=60)
        def my_func(response=None):
            nonlocal calls
            calls += 1
            return "data"

        r1 = DummyResponse()
        r2 = DummyResponse()

        # first call should miss
        result1 = my_func(response=r1)
        self.assertEqual(result1, "data")
        self.assertEqual(r1.headers["X-Cache"], "MISS")
        self.assertEqual(calls, 1)

        # second call should hit without calling function again
        result2 = my_func(response=r2)
        self.assertEqual(result2, "data")
        self.assertEqual(r2.headers["X-Cache"], "HIT")
        self.assertEqual(calls, 1)

    def test_cache_key_with_same_params_hits(self):
        calls = 0

        @cache(expire=60)
        def my_func(params=None, response=None):
            nonlocal calls

            calls += 1
            return params.page

        r1 = DummyResponse()
        r2 = DummyResponse()

        p1 = Params(page=1, page_size=10)
        p2 = Params(page=1, page_size=10)

        my_func(params=p1, response=r1)
        my_func(params=p2, response=r2)

        # should call function only once and handle params: Params as cachhe_key without failing
        self.assertEqual(calls, 1)
        self.assertEqual(r1.headers["X-Cache"], "MISS")
        self.assertEqual(r2.headers["X-Cache"], "HIT")

    def test_cache_miss_with_different_params(self):
        calls = 0

        @cache(expire=60)
        def my_func(params=None, response=None):
            nonlocal calls

            calls += 1
            return params.page

        r1 = DummyResponse()
        r2 = DummyResponse()

        p1 = Params(page=1, page_size=10)
        p2 = Params(page=2, page_size=10)

        my_func(params=p1, response=r1)
        my_func(params=p2, response=r2)

        self.assertEqual(calls, 2)
        self.assertEqual(r2.headers["X-Cache"], "MISS")

    def test_clear_cache_specific_function(self):
        calls = 0

        @cache(expire=60)
        def my_func(response=None):
            nonlocal calls

            calls += 1
            return "data"

        r1 = DummyResponse()
        r2 = DummyResponse()

        my_func(response=r1)
        self.assertEqual(calls, 1)

        clear_cache("my_func")

        my_func(response=r2)
        self.assertEqual(calls, 2)
        self.assertEqual(r2.headers["X-Cache"], "MISS")

    def test_clear_all_cached(self):
        calls = 0

        @cache(expire=60)
        def my_func(response=None):
            nonlocal calls

            calls += 1
            return "data"

        r1 = DummyResponse()
        r2 = DummyResponse()

        my_func(response=r1)
        clear_all_cached()
        my_func(response=r2)

        self.assertEqual(calls, 2)


if __name__ == "__main__":
    unittest.main()
