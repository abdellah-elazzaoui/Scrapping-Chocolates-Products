# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ChocolatescrapperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ChocolatescrapperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


from urllib.parse import urlencode
import requests
from random import randint
import logging
SCRAPEOPS_API_KEY ="3aa02299-e804-42a3-aecc-9e5fe47b1d17"
SCRAPEOPS_FAKE_USERS_AGENTS_ENDPOINTS = "https://headers.scrapeops.io/v1/user-agents"
SCRAPEOPS_FAKE_USERS_AGENTS_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

class ScrapeOpsFakeUserAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoints = settings.get("SCRAPEOPS_FAKE_USERS_AGENTS_ENDPOINTS","https://headers.scrapeops.io/v1/user-agents")
        self.scrapeops_fake_user_agents_enable = settings.get('SCRAPEOPS_FAKE_USERS_AGENTS_ENABLED')
        self.scrapeops_num_result = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.header_list = []
        self.user_agent_list = []
        self._get_user_agent_list()
        self._scrapeops_fake_user_agents_enabled()

    def _get_user_agent_list(self):
        payload = {"api_key": self.scrapeops_api_key}
        if self.scrapeops_num_result is not None:
            payload["num_results"] = self.scrapeops_num_result   # <-- fix: correct param name

        try:
            response = requests.get(self.scrapeops_endpoints, params=payload, timeout=10)
            json_response = response.json()
            self.user_agent_list = json_response.get('result', [])
        except Exception as e:
            print(f"[ScrapeOps Middleware] Failed to fetch user agents: {e}")
            self.user_agent_list = []

    def _get_random_user_agents(self):
        if not self.user_agent_list:
            # fallback user-agent if API fails
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        random_index = randint(0, len(self.user_agent_list) - 1)
        return self.user_agent_list[random_index]

    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_num_result in [None, '', ' ']:
            self.scrapeops_fake_user_agents_enable = False
        else:
            self.scrapeops_fake_user_agents_enable = True

    def process_request(self, request, spider):
            random_user_agent = self._get_random_user_agents()
            request.headers['User-Agent'] = random_user_agent

            spider.logger.info("*************** NEW HEADER ATTACHED *************")
            spider.logger.info(f"User-Agent: {random_user_agent}")
