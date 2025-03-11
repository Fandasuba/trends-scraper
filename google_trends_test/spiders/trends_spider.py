from pathlib import Path
import time
import scrapy

class TrendsSpider(scrapy.Spider):
    name = "trends"
    
    def start_requests(self):
        geo = "GB"
        category = "17"
        hours = "24"
        
     # Adjust link later. For nw its a dummy link for testing purposes.
        url = f"https://trends.google.com/trends/trendingsearches/daily?geo={geo}&cat={category}&hl=en-GB"
        yield scrapy.Request(url=url, callback=self.parse)
    
    ### Ignore code below for now. Time to learn splash bozo since it doesnt seem to want to render the Javascript.
    def parse(self, response):
        time.sleep(5)
        
      
        filename = "trends_test.html"
        Path(filename).write_bytes(response.body)
        
        # Look for the container
        container = response.xpath('/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]')
        
        if container:
            yield container
        else:
            self.logger.error("Could not find the trends container. Check the saved HTML to verify the structure.")
   