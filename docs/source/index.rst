.. OWASP Maryam documentation master file, created by
   sphinx-quickstart on Thu May 27 12:13:59 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

************
OWASP Maryam
************

Open-source intelligence(OSINT) is a method of using open source tools to collect
information and analyze them for a specific purpose. OSINT can be very helpful for
hackers to use to garner data about particular organizations. Today, using
open-sources like bing, google, yahoo, etc.., for data gathering is one of the important
steps for reconnaissance and this is a common task. It should be a tool to automate this
routine. One of the best tools in this field is The OWASP Maryam.

`github <https://github.com/saeeddhqan/Maryam>`_

Introduction
############

OWASP Maryam is a modular/optional open-source framework based on OSINT and data gathering. Maryam is written in the Python programming language and has been designed to provide a powerful environment to harvest data from open sources and search engines and collect data quickly and thoroughly.

Getting Started
###############


Install
#######

 **From pip**

You can install maryam by pip:
::
   pip install maryam

**From source**

The repository can be loaded using the following command:
::
 git clone https://github.com/saeeddhqan/maryam.git
 cd maryam


The next step is to install the requirements
::
 pip3 install -r requirements
 python setup.py install

The installation is finished and you can run with:
::
 maryam


**Update**

If it already exists, these commands remove the old version completely and replace it
with the new version. From the Maryam install directory:
::
 cd ..
 rm -rf maryam
 git clone https://github.com/saeeddhqan/maryam.git
 cd maryam
 python setup.py install
 maryam

And these commands, update the remote URL of the current repository. From the
Maryam install directory:
::
 git remote set-url origin https://github.com/saeeddhqan/maryam.git
 git reset --hard HEAD~1
 git pull
