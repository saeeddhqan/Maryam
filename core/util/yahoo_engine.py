# -*- coding: utf-8 -*-


class yahoo_engine:
    """docstring for yahoo_engine"""

    def __init__(self, framework, word, limit, count, agent, timeout, cookie, proxy):
        self.agent = agent
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.framework = framework
        self.word = self.framework.urlib(
            word).quote() if '%' not in word else word
        self.page = ''
        self._pages = ''
        self.yahoo = "www.search.yahoo.com"
        self.count = 100 if count > 100 else count
        self.limit = 15 if limit > 15 else limit
        self.num = 1

    def searcher(self):
        url = "http://%s/search?p=%s&b=%d&pz=%d" % (
            self.yahoo, self.word, self.num, self.count)
        try:
            req = self.framework.request(
                url=url,
                cookie=self.cookie,
                agent=self.agent,
                proxy=self.proxy,
                timeout=self.timeout)
        except Exception as e:
            self.framework.error("Connection Error: " + e.message)
        else:
            self.page = req.text
            self._pages += self.page

    def run_crawl(self):
        while(self.num <= self.limit):
            self.searcher()
            self.num += 1

    @property
    def get_pages(self):
        return self._pages
