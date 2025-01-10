import unittest
from research_papers_fetcher import fetch_papers

class TestFetchPapers(unittest.TestCase):

    def test_fetch_paper_ids(self):
        ids = fetch_papers.fetch_paper_ids('cancer')
        self.assertTrue(isinstance(ids, list))

    def test_filter_papers(self):
        papers = [
            {'uid': '12345', 'authors': [{'name': 'John Doe', 'affiliation': 'Pharma Inc.'}]}
        ]
        filtered = fetch_papers.filter_papers(papers)
        self.assertTrue(len(filtered) > 0)

if __name__ == '__main__':
    unittest.main()
