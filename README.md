[![Build Status](https://app.travis-ci.com/saeeddhqan/Maryam.svg?branch=master)](https://app.travis-ci.com/github/saeeddhqan/Maryam)
![Version 2.5.1](https://img.shields.io/badge/Version-2.5.1-green.svg)
![GPLv3 License](https://img.shields.io/badge/License-GPLv3-green.svg)
![Python 3.10.x](https://img.shields.io/badge/Python-3.10.x-green.svg)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4577/badge)](https://bestpractices.coreinfrastructure.org/projects/4577)

# OWASP Maryam

OWASP Maryam is a modular open-source framework based on OSINT and data gathering. It is designed to provide a robust environment to harvest data from open sources and search engines quickly and thoroughly.

# Installation

### Supported OS
 - Linux
 - FreeBSD
 - Darwin
 - OSX

```bash
$ pip install maryam
```

# Usage

```bash
# Using dns_search. --max means all of resources. --api shows the results as json.
# .. -t means use multi-threading.
maryam -e dns_search -d ibm.com -t 5 --max --api --form 
# Using youtube. -q means query
maryam -e youtube -q "<QUERY>"
maryam -e google -q "<QUERY>"
maryam -e dnsbrute -d domain.tld
# Show framework modules
maryam -e show modules
# Set framework options.
maryam -e set proxy ..
maryam -e set agent ..
maryam -e set timeout ..
# Run web API
maryam -e web api 127.0.0.1 1313
```

# Latest Updates

 - Clustering, Meta Search Engine, Dark-Web Search
 - Iris: the first beta version
 - Added famous_person
 - Core speedup optimizations
 - Added setup.py
 - Web API: web command



# Contribution

Contributes are welcome! Here is a start guide: [Development Guide](https://github.com/saeeddhqan/maryam/wiki/Development-Guide)
You can add a new search engine to the util classes or use the current search engines to write a new module.
The best help to write a new module is checking the current modules.

# Roadmap

 - Write a complete metacrawler engine based on OSINT by using the current search engines
 - Add clustering algorithms: Done
 - Web User Interface

# Links
### [OWASP](https://owasp.org/www-project-maryam/)
### [Wiki](https://github.com/saeeddhqan/maryam/wiki)
### [Install](https://github.com/saeeddhqan/maryam/wiki#install)
### [Modules Guide](https://github.com/saeeddhqan/maryam/wiki/modules)
### [Development Guide](https://github.com/saeeddhqan/maryam/wiki/Development-Guide)

To report bugs, requests, or any other issues please [create an issue](https://github.com/saeeddhqan/maryam/issues).
