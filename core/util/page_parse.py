# -*- coding : u8 -*-
import re as _re


class page_parse:
    """docstring for page_parse"""

    def __init__(self, framework, page):
        self.framework = framework
        self.page = page

    def generic_clean(self):
        self.page = _re.sub(r"<em>", '', self.page)
        self.page = _re.sub(r"<b>", '', self.page)
        self.page = _re.sub(r"</b>", '', self.page)
        self.page = _re.sub(r"</em>", '', self.page)
        self.page = _re.sub(r"%2f", ' ', self.page)
        self.page = _re.sub(r"%3a", ' ', self.page)
        self.page = _re.sub(r"<strong>", '', self.page)
        self.page = _re.sub(r"</strong>", '', self.page)
        self.page = _re.sub(r"<wbr>", '', self.page)
        self.page = _re.sub(r"</wbr>", '', self.page)

    def findall(self, re):
        re = _re.compile(re)
        return re.findall(self.page)

    def get_sites(self):
        self.generic_clean()
        re = _re.compile(r"<cite>(.*?)</cite>")
        resp = []
        for i in re.findall(self.page):
            if(i not in resp):
                resp.append(i)
        return resp

    def get_social_nets(self):
        self.generic_clean()
        reg_id = self.framework.reglib().social_network_ulinks
        resp = {}
        for i in reg_id:
            _id = _re.findall(reg_id[i], self.page)
            _id2 = []
            for j in _id:
                if(j not in _id2):
                    _id2.append(j)
            resp[i] = _id2
        return resp

    def get_emails(self, host):
        self.generic_clean()
        host = host + '.' if '.' not in host else host
        resp = []
        for i in _re.findall(r"[A-z0-9.\-]+@[A-z0-9\-\.]{0,255}?%s(?:[A-z]+)?" % host, self.page):
            if(i not in resp):
                resp.append(i)
        return resp

    def get_dns(self, host):
        self.generic_clean()
        resp = []
        for i in _re.findall(r"[A-z0-9\.\-]+\.%s" % host, self.page):
            i = i.replace("\\", "").replace("www.", "")
            i = i[1:] if i[0] == "." else i
            if(i not in resp):
                resp.append(i)
        return resp
