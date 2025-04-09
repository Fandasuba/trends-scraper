from pathlib import Path
import scrapy
from scrapy_splash import SplashRequest
import json

params = {'geo': 'UK', 'category': '17'}

class TrendsSpider(scrapy.Spider):
    name = "trends"

    params = {'geo': 'GB', 'category': '17'}
   
    def start_requests(self, params):
        geo = params.get('geo', 'US')
        category = params.get('category', '17')

        url = f"https://trends.google.com/trending?geo={geo}&category={category}"
       
        self.logger.info(f"Starting request to {url} via Splash")
       
        yield SplashRequest(
            url=url,
            callback=self.parse,
            endpoint='render.html',
            args={
                'wait': 1.4,  # 1.4 Seems to the fastest based on tests. Anything lower causes it to not return an array filled with data.
                'timeout': 90,
                'images': 0,
                'resource_timeout': 20,
            },
            meta={'dont_redirect': True},
        )
   
    def parse(self, response):
        self.logger.info(f"Response from {response.url} with {response.status} status.")
       
        filename = "trends_test.html"
        Path(filename).write_bytes(response.body)
        self.logger.info(f"Saved response to {filename}")
       
        # Divs with class "mZ3RIc" seem to be the actual trend name that pops up.
        trends_data = []
        for trend in response.css("tr.enOdEe-wZVHld-xMbwt"):
            keyword = trend.css("div.mZ3RIc::text").getall()
            related = trend.css("div.k36WW span.mUIrbf-vQzf8d::text").getall()
            time_ago = trend.css("div.A7jE4::text").get()
            trends_data.append({"keyword": keyword, "related": related, "time_ago": time_ago})
       
        JSONfilename = "trends.json"
        with open(JSONfilename, 'w', encoding='utf-8') as f:
            json.dump(trends_data, f, ensure_ascii=False, indent=4)
        
        self.logger.info(f"Saved {len(trends_data)} trends to {JSONfilename}")
        
        return trends_data