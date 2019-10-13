# -*- coding: u8 -*-

from lxml.html import fromstring
from cookielib import CookieJar
import re
import tempfile
import webbrowser

class google_engine:
    """docstring for google_engine"""

    def __init__(self, framework, word, limit, count, cookie, agent, proxy, timeout):
        self.framework = framework
        self.word = word
        self.cookiejar = CookieJar()
        self.agent = 'Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1'
        self._pages = ''
        self.limit = limit
        # count links in page
        self.num = count
        self._links = []

    def run_crawl(self):
        page = 1
        url = "http://google.com/search"
        payload = {"num" : self.num, "start" : page, "ie" : "utf-8", "oe" : "utf-8", "q" : self.word}
        while True:
            try:
                req = self.framework.request(
                    url=url,
                    payload=payload,
                    redirect=False,
                    cookie=self.cookiejar,
                    agent=self.agent)
            except Exception as e:
                self.framework.error(e)
            else:
                # follow the redirect to the captcha
                count = 0
                while req.status_code == 302:
                    redirect = req.headers['location']
                    # request the captcha page
                    req = self.framework.request(url=redirect, redirect=False, cookie=self.cookiejar, agent=self.agent)
                    count += 1
                    # account for the possibility of infinite redirects
                    if count == 20:
                        break
                # handle the captchapage
                # check needed because the redirect could result in an error
                # will properly exit the loop and fall to the error check below
                if req.status_code == 503:
                    req = self.captcha(req)
                    continue
                # handle error conditions
                if req.status_code in [301, 302]:
                    # follow the redirect to the main page
                    count = 0
                    while req.status_code in [301, 302]:
                        tree = fromstring(req.text)
                        moved_link = tree.xpath("//a/@href")[0]
                        # request the main page
                        req = self.framework.request(url=moved_link, redirect=False, cookie=self.cookiejar, agent=self.agent)
                        count += 1
                        if count == 10:
                            break

                if req.status_code != 200:
                    self.framework.error("Google encountered an unknown error.")
                    break

                self._pages += req.text
                # check limit
                if self.limit == page:
                    break
                page += 1
                payload["start"] = page
                # check for more pages
                if '>Next</' not in req.text:
                    break

    def captcha(self, resp):
        # set up the captcha page markup for parsing
        tree = fromstring(resp.text)
        # extract and request the captcha image
        resp = self.framework.request('https://ipv4.google.com' + tree.xpath('//img/@src')[0], redirect=False, cookie=self.cookiejar, agent=self.agent)
        # store the captcha image to the file system
        with tempfile.NamedTemporaryFile(suffix='.jpg') as fp:
            fp.write(resp.raw)
            fp.flush()
            # open the captcha image for viewing in gui environments
            w = webbrowser.get()
            w.open('file://' + fp.name)
            self.framework.alert(fp.name)
            try:
                _payload = {'captcha': raw_input('[CAPTCHA] Answer: ')}
            except:
                _payload = {'captcha': input('[CAPTCHA] Answer: ')}
            # temporary captcha file removed on close
        # extract the form elements for the capctah answer request
        form = tree.xpath('//form[@action="index"]')[0]
        for x in ['q', 'continue', 'submit']:
            _payload[x] = form.xpath('//input[@name="%s"]/@value' % (x))[0]
        # send the captcha answer
        return self.framework.request('https://ipv4.google.com/sorry/index', payload=_payload, cookiejar=self.cookiejar, agent=self.agent)

    @property
    def get_pages(self):
        return self._pages

    @property
    def get_links(self):
        try:
            tree = fromstring(self._pages)
        except:
            return self._links
        else:
            links = tree.xpath("//a/@href")
            for link in links:
                cond1 = re.compile(r"/url\?q=[^/]").match(link) != None
                cond2 = "http://webcache.googleusercontent.com" not in link
                cond3 = link not in self._links
                if cond1 and cond2 and cond3:
                    link = re.sub(r"/url\?q=", "", link)
                    self._links.append(link)
            return self._links
