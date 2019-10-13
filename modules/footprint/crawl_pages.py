# -*- coding : u8 -*-

from core.module import BaseModule
from lxml.html import fromstring
import re


class Module(BaseModule):

    meta = {
        "name" : "Crawler Pages",
        "author" : "Saeed Dehqan(saeeddhqan)",
        "version" : "0.5",
        "description" : "Search to find Keywords,Emails,Usernames,Errors,META tags and your regex(if is set) on the page/pages",
        "new feature" : "Errors search",
        "options" : (
            ("url", BaseModule._global_options["target"], True, "URL for get sources"),
            ("regex", None, True, "Regex or string for search in pages"),
            ("more", False, True, "Get keywords,emails and .."),
            ("crawl", False, False, "Crawl in the more pages"),
        )
    }

    def module_run(self):
        url = self.options["url"]
        regex = self.options["regex"]
        scrap = self.web_scrap(url=url, multipage=self.options["crawl"])
        scrap.run_crawl()
        pages = scrap.get_pages
        category_pages = scrap.get_category_pages
        # Output flag
        flag = 0

        ## Regular Expression Search ##
        ###############################
        if regex:
            reg_find = {}
            self.alert("Regex search:")
            regex_cmp = re.compile(regex)
            for page in category_pages:
                resp = regex_cmp.findall(category_pages[page])
                self.output("\tRegex \"%s\" search at \"%s\":" % (regex, page))
                for i in resp:
                    if i not in reg_find.keys():
                        reg_find[i] = 1
                    else:
                        reg_find[i] = reg_find[i] + 1

                for i in reg_find:
                    self.output("\t\tFound \"%s\" Repeated %s times" %
                                (i, reg_find[i]), "g")
                if reg_find:
                    if flag == 0:flag = 1
                reg_find = {}

            if flag == 0:
                self.output("\tNo response")


        if not self.options["more"]:
            return

        patterns = ["</HEAD><BODY><HR><H3>Error Occurred While Processing Request</H3><P>",
                    "exceptions.ValueError",
                    "<h2> <i>Runtime Error</i> </h2></span>",
                    "<p>Active Server Pages</font> <font face=\"Arial\" size=2>error \'ASP 0126\'</font>",
                    "<H3>Original Exception: </H3>",
                    "<b> Description: </b>An unhandled exception occurred during the execution of the",
                    "<H1>Error page exception</H1>",
                    "<h2> <i>Access is denied</i> </h2></span>",
                    "Server object error",
                    "invalid literal for int()",
                    "\[an error occurred while processing this directive\]",
                    "<font face=\"Arial\" size=2>error \'800a0005\'</font>",
                    "<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE>",
                    "\[java.lang.",
                    "class java.lang.",
                    "java.lang.NullPointerException",
                    "java.rmi.ServerException",
                    "at java.lang.",
                    "onclick=\"toggle(\'full exception chain stacktrace\')",
                    "at org.apache.catalina",
                    "at org.apache.coyote.",
                    "at org.apache.tomcat.",
                    "at org.apache.jasper.",
                    "<html><head><title>Application Exception</title>",
                    "<p>Microsoft VBScript runtime </font>",
                    "<font face=\"Arial\" size=2>error '800a000d'</font>",
                    "<TITLE>nwwcgi Error",
                    "\] does not contain handler parameter named",
                    "PythonHandler django.core.handlers.modpython",
                    "t = loader.get_template(template_name) # You need to create a 404.html template.",
                    "<h2>Traceback <span>(innermost last)</span></h2>",
                    "<h1 class=\"error_title\">Ruby on Rails application could not be started</h1>",
                    "</b> on line <b>"
                    "<title>Error Occurred While Processing Request</title></head><body><p></p>",
                    "<TR><TD><H4>Error Diagnostic Information</H4><P><P>",
                    "<li>Search the <a href=\"http://www.macromedia.com/support/coldfusion/\"",
                    "target=\"new\">Knowledge Base</a> to find a solution to your problem.</li>",
                    "thrown in <b>",
                    "<h2 style=\"font:8pt/11pt verdana; color:000000\">HTTP 403.6 - Forbidden: IP address rejected<br>",
                    "<TITLE>500 Internal Server Error</TITLE>",
                    "<b>warning</b>[/]\w\/\w\/\S*",
                    "<b>Fatal error</b>:",
                    "<b>Warning</b>:",
                    "open_basedir restriction in effect",
                    "eval()'d code</b> on line <b>",
                    "Server.Execute Error",
                    "Fatal error</b>:  preg_replace",
                    "<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE></HEAD><BODY><HR><H3>",
                    "Stack trace:"]

        page_parse = self.page_parse(pages)
        meta_reg_template = r"<meta %s=[\'\"]{1}%s[\'\"]{1}\scontent=[\'\"]{1}(.{0,255})[\'\"]{1}"

        ## H1 Tags ##
        #############
        # find h1 tags
        try:
            tree = fromstring(pages)
        except:
            pass
        else:
            h1 = tree.xpath("//h1")
            self.alert("H1 tag values:")
            flag = 0
            out = []
            for i in h1:
                value = i.text
                if value not in out:
                    out.append(value)
                    self.output("\t\"%s\"" % value, "g")
                    if flag == 0:flag = 1
            if flag == 0:
                self.output("\t..")
            out = []

        ## META TAG PROPERTY SEARCH ##
        #####################
        meta_propery = ["og:locale", "og:type"]
        self.alert("Meta tag property:")
        flag = 0
        for i in meta_propery:
            reg = meta_reg_template % ("property", i)
            value = page_parse.findall(reg)
            self.output("\tmeta propery \"%s\":" % i)
            for j in value:
                if j not in out:
                    out.append(j)
                    self.output("\t\t\"%s\"" % j, "g")
                    if flag == 0:flag = 1
            if flag == 0:
                self.output("\t\t..")
            else:
                flag = 0
        out = []

        ## META TAG NAME ##
        ###################
        meta_name = ["keywords", "author", "generator"]
        self.alert("Meta tag name:")
        flag = 0
        for i in meta_name:
            reg = meta_reg_template % ("name", i)
            value = page_parse.findall(reg)
            self.output("\tmeta name \"%s\":" % i)
            for j in value:
                if j not in out:
                    out.append(j)
                    self.output("\t\t\"%s\"" % j, "g")
                    if flag == 0:flag = 1
            if flag == 0:
                self.output("\t\t..")

        ## EMAILS ##
        ############
        emails = page_parse.findall(r"\w+@[a-zA-Z_\-.0-9]{5,255}")
        if emails != []:
            self.alert("Emails:")
            for i in emails:
                self.output("\t\"%s\"" % i, "g")

        ## SOCIAL NETWORK ##
        ####################
        ids = page_parse.get_social_nets()
        self.alert("Social Networks:")
        for i in ids:
            self.output("\t%s:" % i.title())
            if(ids[i] != []):
                for j in ids[i]:
                    self.output("\t\t\"%s\"" % j, "g")
            else:
                self.output("\t\t..")
        flag = 0
        ## ERRORS ##
        ############
        self.alert("Errors:")
        for patt in patterns:
            for page in category_pages:
                if re.search(patt, category_pages[page]):
                    self.output("\t\"%s\" found at %s" % (patt, page), "g")
                    if flag == 0:flag = 1

        if flag == 0:
            self.output("\t..")
