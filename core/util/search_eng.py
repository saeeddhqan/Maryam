# -*- coding: utf-8 -*-


class search_eng:
    """docstring for search_eng"""

    def __init__(
            self,
            framework,
            word,
            limit,
            count,
            engines,
            cookie=None,
            agent=None,
            proxy=None,
            timeout=None):
        self.framework = framework
        self.cookie = cookie
        self.agent = agent
        self.proxy = proxy
        self.timeout = timeout
        self.word = word
        self.limit = limit
        self.count = count
        self.engines = engines
        self._engines = ["bing", "google", "yahoo",
                         "yandex", "ask", "metacrawler"]
        self._pages = None

    def run_crawl(self):
        pages = ""
        alert_mode = self.framework._global_options["verbosity"] == 2
        for i in self.engines:
            if(i.lower() in self._engines):
                if(alert_mode):
                    self.framework.alert("Search in \"%s\"" % i)
                try:
                    attr = getattr(self.framework, "%s_engine" % i)(
                        word=self.word,
                        limit=self.limit,
                        count=self.count,
                        cookie=self.cookie,
                        agent=self.agent,
                        proxy=self.proxy,
                        timeout=self.timeout)
                    attr.run_crawl()
                except Exception as e:
                    self.framework.error(e.message)
                else:
                    pages = pages + attr.get_pages
            else:
                if(alert_mode):
                    self.framework.error(
                        "Search Engine \"%s\" Not Found !" % i)

        self._pages = pages

    @property
    def get_pages(self):
        return self._pages
