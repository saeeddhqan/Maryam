# -*- coding: u8 -*-

from lxml.html import fromstring
import re
# Web Scraper v4.1

class web_scrap:
    """docstring for web_scrap"""

    def __init__(self, framework, url, agent,
                 timeout, cookie, proxy, multipage, intime=False):
        self.framework = framework
        self.agent = agent
        self.multipage = multipage
        self.timeout = timeout
        self.cookie = cookie
        self.proxy = proxy
        self.intime = intime
        self.urlib = self.framework.urlib
        # ADD http:// 
        self.url = self.urlib(url).sub_service(serv="http")
        self._category_pages = {}
        self._pages = ''
        self._links = []
        self._external_links = []
        self._query_links = []
        self._phones = []
        self._css = []
        self._js = []
        self._cdn = []
        self._comments = []

    def run_crawl(self):
        final_links = []
        def intime(val):
            if self.intime:
                self.framework.output(val)

        def cdn_add(link):
            cond = link[:2] == "//" and '.' in link and link not in self._cdn
            if cond:
                self._cdn.append(link)
                return True

        def phone_add(link):
            cond = link[:6] == "tel://"
            if cond:
                self._phones.append(link)
                return True

        # If key not in links append it
        def notin(key, _list):
            if key not in _list:
                _list.append(key)
            return _list

        def url_creator(url, baseurl):
            url = str(url)
            # ADD slash to end url
            url2 = baseurl+'/' if not baseurl.endswith("/") else baseurl
            urparse = self.urlib(url)
            urparse.url = urparse.quote() if '%' not in url else url
            urparse2 = self.urlib(url2)
            cond1 = url in ("%20", '', '/', "%23")
            cond2 = len(
                urparse.url) > 1 and urparse.get_scheme == "" and "%3a//" not in urparse.url.lower() and urparse.url[:2] != "//"
            cond3 = urparse.url[:2] == "//"
            if cond1:
                return False
            elif cond2:
                url = url[1:] if url[0] == '/' else url
                urparse.url = urparse2.join(url)
            elif cond3:
                urparse.url = url
            else:
                urparse.url = url
            url = urparse.url+'/' if not urparse.url.endswith("/") else urparse.url
            return url

        self.url = url_creator(self.url, self.url)

        # Get Data from URL and parse it
        def get_source(url, baseurl):
            links = []
            # Send Request
            try:
                req = self.framework.request(
                    url=url,
                    cookie=self.cookie,
                    agent=self.agent,
                    proxy=self.proxy,
                    timeout=self.timeout)
            except Exception as e:
                return False
            else:
                if req.status_code != 200:
                    return False
                else:
                    resp = req.text

            # if resp is "" return false
            try:
                tree = fromstring(resp)
            except:
                return False

            # ADD Comments
            self._comments.extend(re.findall("<!--(.*?)-->", resp))

            # ADD JS and CSS files
            get_js = tree.xpath("//script/@src")
            get_css = tree.xpath("//link/@href")
            for i in get_js:
                if i.endswith(".js"):
                    i = url_creator(i, baseurl)
                    if i:
                        intime(i)
                        cdn_add(i)
                        notin(i, self._js)

            for i in get_css:
                if i.endswith(".css"):
                    i = url_creator(i, baseurl)
                    if i:
                        intime(i)
                        cdn_add(i)
                        notin(i, self._css)

            get_a = tree.xpath('//a/@href')

            for i in get_a:
                # join url
                i = url_creator(i, baseurl)
                if not i:
                    continue
                intime(i)

                # ADD CDN link and Phone number
                if cdn_add(i) or phone_add(i):
                    continue
                urparse = self.urlib(i)

                # if the link is external link, append it to self._external..
                if urparse.get_netloc.lower() not in self.url.lower():
                    notin(i, self._external_links)
                    continue
                # if the link is query link, append it to self._query..
                if urparse.get_query != "":
                    notin(str(i), self._query_links)

                # at the end, append link to links and ..
                notin(i, links)
                notin(i, final_links)

            if resp != "":
                self._pages = self._pages + resp
                self._category_pages[url] = resp
            return links

        lnks = get_source(self.url, self.url)
        if not lnks:
            return [self.url]
        elif lnks is not []:
            notin(self.url, final_links)


        # if multipage is false: search at one page else: search at more page
        if not self.multipage:
            self._links = final_links
            return

        for i in lnks:
            lnks1 = get_source(i, i)
            if not lnks1:
                continue
            for j in lnks1:
                lnks2 = get_source(j, i)
                if not lnks2:
                    continue
                for k in lnks2:
                    lnks3 = get_source(k, j)
                    if not lnks3:
                        continue

        self._links = final_links


    @property
    def get_pages(self):
        return self._pages

    @property
    def get_category_pages(self):
        return self._category_pages

    @property
    def get_links(self):
        return self._links

    @property
    def get_external_links(self):
        return self._external_links

    @property
    def get_query_links(self):
        return self._query_links

    @property
    def get_js(self):
        return self._js

    @property
    def get_css(self):
        return self._css

    @property
    def get_cdn(self):
        return self._cdn

    @property
    def get_phones(self):
        return self._phones

    @property
    def get_comments(self):
        return self._comments
