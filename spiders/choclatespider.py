import scrapy
from ..items import ChocolateItems
from urllib.parse import urlencode

API_KEY ="API-KEY"
FAKE_USERS_AGENTS_ENDPOINT = "####"
FAKE_USERS_AGENTS_ENABLED = True
NUM_RESULTS = 50
def get_proxy_url(url):
    payload = {"api_key":API_KEY,"url":url}
    proxy_url = "#####" + urlencode(payload)
    return proxy_url

class ChoclatespiderSpider(scrapy.Spider):
    name = "choclatespider"
    allowed_domains = ["www.chocolate.co.uk","proxy.scrapeops.io"]
    start_urls = ["https://www.chocolate.co.uk/collections/all-products"]

    custom_settings={
        "FEEDS":{
            "data.json":{"format":'json',"overrite":True}
        }
    }

    #def start_requests(self):
    #    yield scrapy.Request(url=get_proxy_url(self.start_urls[0]),callback=self.parse)

    
    def parse(self, response):
        books = response.css("product-item.product-item")
        for book in books:
            product = ChocolateItems()
            product["title"] = book.css("div.product-item-meta a::text").get(),
            product["price"] = book.css("span.price::text").getall()[1],
            product["url"  ] = book.css("div.product-item-meta a").attrib["href"]
            yield product
         
        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
            next_page = "https://www.chocolate.co.uk"+next_page
            #yield response.follow(next_page,callback=self.parse)
            yield scrapy.Request(url=next_page,callback=self.parse)
         
    
