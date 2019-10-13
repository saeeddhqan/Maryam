# -*- coding : utf-8 -*-

from core.module import BaseModule
import re
import os


class Module(BaseModule):

    meta = {
        "name": "DNS Searcher",
        "author": "Saeed Dehqan(saeeddhqan)",
        "version": "1.0",
        "description": "Search in search engines and other sources for find DNS. engines[bing,google,yahoo,yandex,metacrawler,ask]",
        "comments": [
            "Sources:search engines and dnsdumpster.com, threatcrowd.org, netcraft.com"
        ],
        "options": (
            ("host", BaseModule._global_options["target"],
             True, "Host name without https?://"),
            ("limit", 3, True, "Search limit(min=1, max=15)"),
            ("count", 50, True, "Link count in page(min=10, max=100)"),
            ("engines", None, False, "Search engine names. e.g bing,google,.."),
            ("threatcrowd", False, True, "Use ThreatCrowd.org"),
            ("netcraft", False, True, "Use NetCraft.org"),
            ("tld", False, True, "DNS tld brute force"),
            ("tldverbose", 349, True, "tld brute force verbose(min=1, max=349)"),
            ("dnsdumpster", False, False, "Uses dnsdumpster.com for get DNS map"),
            ("dnsbrute", False, True, "DNS brute force flag"),
            ("wordlist", os.path.join(BaseModule.data_path, 'dnsnames.txt'), False, "DNS brute force list"),
        )
    }

    def module_run(self):
        host = self.options["host"]
        host_attr = self.urlib(host)
        host = host_attr.sub_service("http")
        hostname = self.urlib(host).get_netloc
        if self.options["engines"]:
            limit = self.options["limit"]
            count = self.options["count"]
            engines = self.options["engines"].split(",")
            run = self.search_eng(hostname, engines, limit, count)
            run.run_crawl()
            page = self.urlib(run.get_pages).unquote()
            dns = self.page_parse(page).get_dns(hostname)
            self.heading("Search Engines:", level=0)
            for i in dns:
                self.output("\t\"%s\"" % i, "G")



        ## NetCraft.com Search #
        ########################
        if self.options["netcraft"]:
            run = self.netcraft_search(hostname)
            run.run_crawl()
            resp = run.get_dns()
            self.heading("NetCraft.com", level=0)
            if resp == []:
                self.output("\tNo Result")
            else:
                for i in resp:
                    self.output("\t\"%s\"" % i, "G")
            del resp,run

        # ThreatCrowd.org Search #
        ##########################
        if self.options["threatcrowd"]:
            final_resp = []
            req = self.request(
                "https://threatcrowd.org/searchApi/v2/domain/report/?domain=" + hostname)
            # print(req.json)
            txt = re.sub("[\t\n ]+", "", req.text)
            txt = re.findall(
                r"\"subdomains\":(\[[\"\.A-z0-9_\-,]+\])", txt)
            resp = txt[0][1:-1].split(",")
            self.heading("ThreatCrowd.org", level=0)
            for i in resp:
                i = i.replace("..", ".")
                if i not in final_resp:
                    final_resp.append(i)
                    self.output("\t%s" % i, "G")
            del final_resp,resp,txt

        ### TLD Brute Force ####
        ########################
        if self.options["tld"]:
            # Full version of http://data.iana.org/TLD/tlds-alpha-by-domain.txt
            tld_list = os.path.join(BaseModule.data_path, 'tlds.txt')
            with open(tld_list) as o:
                tlds = o.read().split()

            hostname = host.split('.')[0]
            self.heading("DNS TLD Brute Furce", level=0)
            tld_verbose = self.options["tldverbose"]
            tld_ver = 349 if tld_verbose > 349 else tld_verbose
            tld_ver = 1 if tld_ver < 1 else tld_ver
            for i in range(0, len(tlds[:tld_ver])):
                tmp_hname = "%s.%s" % (hostname, tlds[i])
                try:
                    req = self.request(tmp_hname)
                except Exception:
                    pass
                else:
                    self.output("\"%s\"" % tmp_hname, "g")
                    

        ##### DNSDUMPSTER.com ######
        ########################
        if self.options["dnsdumpster"]:
            try:
                req = self.request(
                    "https://dnsdumpster.com/static/map/%s.png" % hostname)
            except Exception as e:
                self.verbose(e.args[0], "R")
            else:
                text = req.read
                file_path = "%s/%s.png" % (self.workspace, hostname)
                try:
                    with open(file_path, "wb") as o:
                        o.write(text)
                except Exception as e:
                    self.error("File save error: " + e.message)
                else:
                    self.heading("dnsdumpster.com", level=0)
                    self.output(
                        "\tdnsdumpster response saved in \"%s\"" % file_path)


        ### DNS Brute Force ####
        ########################
        if self.options["dnsbrute"]:
            hits = []
            max_attempt = 4
            attempt = 0
            filename = self.options["wordlist"]
            with open(filename) as o:
                read = o.read().split()
            self.heading("DNS Brute", level=0)
            for i in read:
                if(attempt > max_attempt):
                    break
                tmp_name = "%s.%s" % (i, hostname)
                try:
                    req = self.request(tmp_name)
                except Exception as e:
                    if(e.args[0] == "timed out"):
                        self.verbose("%s => Timed out" % tmp_name, "O")
                        attempt += 1
                    else:
                        self.verbose("%s:\"%s\"" % (e.args[0], tmp_name), "O")
                else:
                    self.output("\"%s\"" % tmp_name, "G")
                    hits.append(tmp_name)
            self.heading("HITS", level=1)
            for i in hits:
                self.output("\t%s" % tmp_name, "G")
