import unittest
from unittest.mock import patch, MagicMock
from jarvis.modules.research_web import WebResearch

class TestWebResearch(unittest.TestCase):
    def setUp(self):
        self.research = WebResearch()

    @patch('jarvis.modules.research_web.requests.get')
    def test_search_and_summarize(self, mock_get):
        # Mock DuckDuckGo API response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'AbstractText': 'Test summary',
            'AbstractURL': 'https://example.com'
        }
        mock_get.return_value = mock_resp
        results = self.research.search('test query')
        summary = self.research.summarize(results)
        self.assertIn('Test summary', summary)
        self.assertIn('https://example.com', summary)
        self.assertIsInstance(summary, str)

if __name__ == '__main__':
    unittest.main()