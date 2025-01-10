import unittest
from research_papers_fetcher import utils

class TestUtils(unittest.TestCase):

    def test_make_request(self):
        result = utils.make_request("https://httpbin.org/get", {"test": "data"})
        self.assertIn('args', result)
        self.assertEqual(result['args']['test'], 'data')

if __name__ == '__main__':
    unittest.main()
