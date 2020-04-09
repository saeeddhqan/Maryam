![Version 1.4.5](https://img.shields.io/badge/Version-1.4.5-green.svg)
[![GPLv3 License](https://img.shields.io/badge/License-GPLv3-red.svg)
![Python 3.x](https://img.shields.io/badge/Python-3.x-green.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/40d81c48b3444ee78ffc6c5c8639134c)](https://www.codacy.com/manual/saeeddhqan/Maryam?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=saeeddhqan/Maryam&amp;utm_campaign=Badge_Grade)

<img src="https://owasp.org/assets/images/logo.png">

# OWASP Maryam

[![asciicast](https://asciinema.org/a/316888.svg)](https://asciinema.org/a/316888)

OWASP Maryam is an Open-source intelligence(OSINT) and Web-based Footprinting modular/tool framework based on the Recon-ng and written in Python.
If you have skill in Metasploit or Recon-ng, you can easily use it without prerequisites. And if not, please read the [Quick Guide](https://github.com/saeeddhqan/Maryam/wiki#quick-guide).

## Tools
**OSINT**

 - dns_search
	> Search in the search engines and other sources for find DNS.
 - email_search
	> Search in search engines for find emails.
 - docs_search
	> Search in engines for find related documents. 
 - onion_search
	> onion_search is to create the premier search engine for services residing on the Tor anonymity network.
 - godork	
	> Search your dork in the google and get result
 - social_nets
	> Search for find usernames in social networks.
 - crawler
	> Crawl web pages for find links, JS Files, CSS files, Comments And everything else interesting with thread supporting
	
**FOOTPRINT**
 - crawl_pages
	> Search to find keywords, emails, usernames, errors, meta tags and regex on the page/pages
 - dbrute 
	> DNS brute force attack with thread supporting
 - fbrute 
	> File/Directory brute force attack with thread supporting
 - tldbrute
	> TLD brute force attack with thread supporting
 - waf
	> Identify web application firewalls. It can detect over 200 firewall
 - wapps        
	> Web fingerprinting to identify the applications used with over 1000 pyload.
 - interest_files
	> Search hosts for interesting files in predictable locations and brute force it.
 - entry_points
	> Crawl web pages for find entry points(inputs, urls with param)

**SEARCH**
 - google
	> Google.com search
 - metacrawler 
	> Metacrawler.com search
 - yippy 
	> Yippy.com search
 - crt
	> Crt.sh search
 - carrot2
	> carrot2.org search
 - bing
	> bing.com search
 - twitter
	> twitter.com search
 - linkedin
	> linkedin.com search

## News
**What is news in 1.4.5?**

 - Using python3
 - Added dbrute, fbrute, tldbrute, entry_points and waf to footprint
 - Added Thread supporting to modules
 - Added csv format output
 - Rewrite utils
 
## links
### [OWASP](https://owasp.org/www-project-maryam/)
### [Wiki](https://github.com/saeeddhqan/maryam/wiki)
### [Install](https://github.com/saeeddhqan/maryam/wiki#install)
### [Modules Guide](https://github.com/saeeddhqan/maryam/wiki/modules)
### [Development Guide](https://github.com/saeeddhqan/maryam/wiki/Development-Guide)

Bugs, requests, or any other issues please [contact me](mailto:saeed.dehghan@owasp.org)
