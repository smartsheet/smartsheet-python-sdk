import unittest
import warnings
import ssl
from smartsheet.session import _SSLAdapter

class TestSSLContext(unittest.TestCase):

    def test_no_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            adapter = _SSLAdapter()
            context = adapter.create_ssl_context()
            self.assertEqual(len(w), 0, "Deprecation warning was raised")

if __name__ == "__main__":
    unittest.main()
