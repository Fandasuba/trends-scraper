import unittest
from unittest import mock
from pathlib import Path
import json
from scrapy.http import HtmlResponse, Request
from google_trends_test.spiders.trends_spider import TrendsSpider

class TrendsScraperTest(unittest.TestCase):
    
    def setUp(self):
        self.spider = TrendsSpider()
        
        # Dummy HTML
        self.dummy_html = """
        <html>
        <body>
            <table>
                <tr class="enOdEe-wZVHld-xMbwt">
                    <td>
                        <div class="mZ3RIc">manchester united</div>
                        <div class="A7jE4">3h ago</div>
                    </td>
                </tr>
                <tr class="enOdEe-wZVHld-xMbwt">
                    <td>
                        <div class="mZ3RIc">liverpool vs arsenal</div>
                        <div class="A7jE4">5h ago</div>
                    </td>
                </tr>
                <tr class="enOdEe-wZVHld-xMbwt">
                    <td>
                        <div class="mZ3RIc">premier league</div>
                        <div class="A7jE4">12h ago</div>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
    def test_parse_finds_expected_trends(self):
        response = HtmlResponse(
            url='https://trends.google.com/trending?geo=GB&category=17',
            body=self.dummy_html.encode('utf-8'),
            encoding='utf-8',
            request=Request(url='https://trends.google.com/trending?geo=GB&category=17')
        )
        
        # Mock file operations to avoid writing actual files during testing
        with mock.patch('pathlib.Path.write_bytes'), \
             mock.patch('builtins.open', mock.mock_open()), \
             mock.patch('json.dump'):
            
            results = self.spider.parse(response)
            self.assertEqual(len(results), 3)
            expected_keywords = [
                ['manchester united'], 
                ['liverpool vs arsenal'], 
                ['premier league']
            ]
            
            expected_times = ['3h ago', '5h ago', '12h ago']

            for i, result in enumerate(results):
                self.assertEqual(result['keyword'], expected_keywords[i])
                self.assertEqual(result['time_ago'], expected_times[i])

if __name__ == '__main__':
    unittest.main()