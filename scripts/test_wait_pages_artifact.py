import unittest
from unittest.mock import Mock
from urllib.error import HTTPError
from wait_pages_artifact import wait_for_artifact


def artifact(id=42, **kw):
    return dict(id=id, name='github-pages', size_in_bytes=100, expired=False, **kw)


class ReadinessTest(unittest.TestCase):
    def test_delayed_visibility(self):
        fetch = Mock(side_effect=[[], [artifact(41)], [artifact()]])
        sleep = Mock()
        wait_for_artifact(fetch, '42', attempts=3, sleep=sleep)
        self.assertEqual(sleep.call_count, 2)

    def test_never_visible(self):
        with self.assertRaises(TimeoutError):
            wait_for_artifact(lambda: [], '42', attempts=2, sleep=lambda _: None)

    def test_transient_server_error(self):
        fetch = Mock(side_effect=[HTTPError('url', 503, 'unavailable', {}, None), [artifact()]])
        wait_for_artifact(fetch, '42', sleep=lambda _: None)

    def test_permission_error_fails_immediately(self):
        fetch = Mock(side_effect=HTTPError('url', 403, 'forbidden', {}, None))
        with self.assertRaises(HTTPError):
            wait_for_artifact(fetch, '42', sleep=lambda _: self.fail('must not retry'))

    def test_invalid_artifacts(self):
        for rows in [[artifact(), artifact(43)], [{**artifact(), 'expired': True}], [{**artifact(), 'size_in_bytes': 0}]]:
            with self.subTest(rows=rows), self.assertRaises(RuntimeError):
                wait_for_artifact(lambda: rows, '42')


if __name__ == '__main__':
    unittest.main()
