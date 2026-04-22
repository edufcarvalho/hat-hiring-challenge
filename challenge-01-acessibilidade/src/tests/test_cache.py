import unittest

from src.domain.schemas import Params
from src.infra.cache import cache, clear_all_cached, clear_cache


class DummyResponse:
    def __init__(self):
        self.headers = {}


class TestCache(unittest.TestCase):
    # flush cache to ensure no colisions between tests
    def tearDown(self):
        clear_all_cached()

    def test_cache_hit_and_miss(self):
        calls = 0

        @cache()
        def my_func(response=None):
            nonlocal calls
            calls += 1
            return "data"

        r1 = DummyResponse()
        r2 = DummyResponse()

        miss = my_func(response=r1)
        hit = my_func(response=r2)

        # first call should miss
        self.assertEqual(miss, "data", "First call should return 'data'")
        self.assertEqual(
            r1.headers["X-Cache"], "MISS", "First call should be a cache MISS"
        )
        self.assertEqual(calls, 1, "Function should be called once for the first call")

        # second call should hit without calling function again
        self.assertEqual(hit, "data", "Second call should return 'data'")
        self.assertEqual(
            r2.headers["X-Cache"], "HIT", "Second call should be a cache HIT"
        )
        self.assertEqual(
            calls, 1, "Function should not be called again for the second call"
        )

    def test_cache_key_with_same_params_hits(self):
        calls = 0

        @cache()
        def my_func(params=None, response=None):
            nonlocal calls

            calls += 1
            return params.page

        miss = DummyResponse()
        hit = DummyResponse()

        p1 = Params(page=1, page_size=10)
        p2 = Params(page=1, page_size=10)

        my_func(params=p1, response=miss)
        my_func(params=p2, response=hit)

        # should call function only once and handle params: Params as cachhe_key without failing
        self.assertEqual(
            calls, 1, "Function should be called only once for same params"
        )
        self.assertEqual(
            miss.headers["X-Cache"], "MISS", "First call should be a cache MISS"
        )
        self.assertEqual(
            hit.headers["X-Cache"],
            "HIT",
            "Second call with same params should be a cache HIT",
        )

    def test_cache_miss_with_different_params(self):
        calls = 0

        @cache()
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

        # all of them should miss (no collision on params) and the function should be called twice
        self.assertEqual(
            calls, 2, "Function should be called twice for different params"
        )
        self.assertEqual(
            r1.headers["X-Cache"], "MISS", "First call should be a cache MISS"
        )
        self.assertEqual(
            r2.headers["X-Cache"],
            "MISS",
            "Second call with different params should be a cache MISS",
        )

    def test_clear_cache_specific_function(self):
        calls = 0

        @cache()
        def my_func(response=None):
            nonlocal calls

            calls += 1
            return "data"

        r1 = DummyResponse()
        r2 = DummyResponse()

        my_func(response=r1)
        self.assertEqual(calls, 1, "Function should be called once initially")

        clear_cache("my_func")

        # all of them should miss because of cache rejection
        my_func(response=r2)
        self.assertEqual(
            calls, 2, "Function should be called again after clearing cache"
        )
        self.assertEqual(
            r1.headers["X-Cache"], "MISS", "First call should be a cache MISS"
        )
        self.assertEqual(
            r2.headers["X-Cache"],
            "MISS",
            "Second call after clearing should be a cache MISS",
        )

    def test_clear_all_cached(self):
        calls = [0, 0]

        @cache()
        def my_func(response=None):
            nonlocal calls

            calls[0] += 1
            return "data"

        @cache()
        def my_func2(response=None):
            nonlocal calls

            calls[1] += 1
            return "data2"

        r1 = DummyResponse()
        r2 = DummyResponse()

        my_func(response=r1)
        my_func2(response=r2)

        clear_all_cached()

        my_func(response=r1)
        my_func2(response=r2)

        self.assertEqual(
            my_func.cache_info().hits,
            0,
            "my_func should have 0 hits after clearing all cache",
        )
        self.assertEqual(
            my_func2.cache_info().hits,
            0,
            "my_func2 should have 0 hits after clearing all cache",
        )
        self.assertEqual(sum(calls), 4, "should call 4 times because never HITs")


if __name__ == "__main__":
    unittest.main()
