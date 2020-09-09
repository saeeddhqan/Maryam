![Version 1.4.7](https://img.shields.io/badge/Version-1.4.7-green.svg)
[![GPLv3 License](https://img.shields.io/badge/License-GPLv3-red.svg)
![Python 3.x](https://img.shields.io/badge/Python-3.x-green.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/40d81c48b3444ee78ffc6c5c8639134c)](https://www.codacy.com/manual/saeeddhqan/Maryam?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=saeeddhqan/Maryam&amp;utm_campaign=Badge_Grade)

<img src="https://owasp.org/assets/images/logo.png">

# OWASP Maryam

[![asciicast](https://asciinema.org/a/357588.svg)](https://asciinema.org/a/357588)

OWASP Maryam is an Open-source intelligence(OSINT) and Web-based Footprinting optional/modular framework based on the Recon-ng core and written in Python.
If you have skill in Metasploit or Recon-ng, you can easily use it without prerequisites and if not, please read the [Quick Guide](https://github.com/saeeddhqan/Maryam/wiki#quick-guide).

<b>Follow the project on [Twitter](https://twitter.com/OWASP_Maryam).</b>

## Modules
**OSINT**

 - dns_search
	> Search in the open-sources to find subdomans.
 - email_search
	> Search in open-sources to find emails.
 - docs_search
	> Search in open-sources to find relevant documents. filetypes[pdf,doc,docx,ppt,pptx,xlsx,txt,..].
 - onion_search
	> onion_search is used to create the premier search engine for services residing on the Tor anonymity network.
 - godork	
	> Search google for your dork and get result.
 - social_nets
	> Search to find usernames in social networks.
 - crawler
	> Crawl web pages to find links, JS Files, CSS files, Comments and everything else interesting, supports concurrency.
 - suggest
 	> Keyword autocompleter to find suggestions in search engines.
	
**FOOTPRINT**
 - crawl_pages
	> Search to find keywords, emails, usernames, errors, meta tags and regex on the page/pages.
 - dbrute 
	> DNS brute force attack, supports concurrency.
 - fbrute 
	> File/Directory brute force attack, supports concurrency.
 - tldbrute
	> TLD brute force attack, supports cocurrency.
 - waf
	> Identify web application firewalls. It can detect over 200 firewalls.
 - wapps        
	> Web fingerprinting to identify the applications used with over 1000 pyload.
 - interest_files
	> Search hosts for interesting files in predictable locations and brute force it.
 - entry_points
	> Crawl web pages to find entry points(inputs, urls with param).

**SEARCH**
 - google
	> Google.com search.
 - metacrawler 
	> Metacrawler.com search.
 - yippy 
	> Yippy.com search.
 - crt
	> Crt.sh search.
 - carrot2
	> Carrot2.org search.
 - bing
	> Bing.com search.
 - twitter
	> Twitter.com search.
 - linkedin
	> Linkedin.com search.
 - facebook
	> Facebook.com search.
 - searchencrypt
	> Searchencrypt.com search.
 - millionshort
	> Millionshort.com search.
 - qwant
	> Qwant.com search.
## News
**What is new?**

 - Uses python3
 - Added dbrute, fbrute, tldbrute, entry_points and waf to footprint
 - Added Thread support to modules
 - Added csv format output
 - Rewrote utils
 - Added Search submodule
 
## links
### [OWASP](https://owasp.org/www-project-maryam/)
### [Wiki](https://github.com/saeeddhqan/maryam/wiki)
### [Install](https://github.com/saeeddhqan/maryam/wiki#install)
### [Modules Guide](https://github.com/saeeddhqan/maryam/wiki/modules)
### [Development Guide](https://github.com/saeeddhqan/maryam/wiki/Development-Guide)

To report bugs, requests, or any other issues please [create an issue](https://github.com/saeeddhqan/maryam/issues).
