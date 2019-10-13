# -*- coding: utf-8 -*-


class hunter_engine:

    def __init__(self, framework, word, key, limit, agent, timeout, cookie, proxy):
        self.agent = agent
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.framework = framework
        self.word = self.framework.urlib(word).quote() if '%' not in word else word  
        self.limit = str(limit)
        self.key = key
        self.page = ''
        self._pages = ''
        self._json_pages = ''
        self.hunter_api = "https://api.hunter.io/v2/domain-search?domain=" + self.word + "&api_key=" + str(self.key) + "&limit=" + str(self.limit)

    def searcher(self):
        try:
            req = self.framework.request(
                url=self.hunter_api,
                cookie=self.cookie,
                agent=self.agent,
                proxy=self.proxy,
                timeout=self.timeout)
        except Exception as e:
            self.framework.error("Connection Error: " + e.message)
        else:
            self.page = req.text
            self._pages += self.page
            self._json_pages = req.json

    def run_crawl(self):
        self.searcher()

    @property
    def get_emails(self):
        emails = self.framework.page_parse(self._pages).get_emails(self.word)
        return emails

    @property
    def get_dns(self):
        dns = self.framework.page_parse(self._pages).get_dns(self.word)
        return dns

    @property
    def get_pages(self):
        return self._pages

    @property
    def get_json_pages(self):
        return self._json_pages
    
