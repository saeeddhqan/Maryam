# -*- coding: utf-8 -*-


class ask_engine:
    """docstring for ask_engine"""

    def __init__(self, framework, word, limit, count, agent, timeout, cookie, proxy):
        self.framework = framework
        self.agent = agent
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.word = self.framework.urlib(
            word).quote() if '%' not in word else word
        self.page = ''
        self._pages = ''
        self.ask = "www.ask.com"
        self.count = 100 if count > 100 else count
        self.limit = 15 if limit > 15 else limit
        self.num = 1

    def searcher(self):
        url = "https://%s/web?q=%s&page=%d" % (self.ask, self.word, self.num)
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

    def next(self):
        nextres = self.framework.page_parse(self.page).findall(r"> Next <")
        if nextres != []:
            nexty = '1'
        else:
            nexty = '0'
        return nexty

    def run_crawl(self):
        while(self.num <= self.limit):
            self.searcher()
            more = self.next()
            if more == '1':
                self.num += 1
            else:
                break

    @property
    def get_pages(self):
        return self._pages
