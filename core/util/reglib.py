#! /usr/bin/python
# -*- coding: u8 -*-
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re


class reglib:
    """docstring for reglib"""

    def __init__(self):
        self.protocol_s = r"^([A-z0-9]+:\/\/)"
        self.protocol_m = r"([A-z0-9]+:\/\/)"
        self.email_s = r"^\w+@[A-z_\-.0-9]{5,255}$"
        self.email_m = r"\w+@[A-z_\-.0-9]{5,255}"
        self.phone_s = r"^([0-9]( |-)?)?(\(?[0-9]{3}\)?|[0-9]{3})( |-)?([0-9]{3}( |-)?[0-9]{4}|[A-z0-9]{7})$"
        self.phone_m = r"([0-9]( |-)?)?(\(?[0-9]{3}\)?|[0-9]{3})( |-)?([0-9]{3}( |-)?[0-9]{4}|[A-z0-9]{7})"
        self.domain_s = r"^([A-z0-9]([A-z0-9\-]{0,61}[A-z0-9])?\.)+[A-z]{2,6}(\:[0-9]{1,5})*$"
        self.domain_m = r"[A-z0-9\-]{0,61}\.+[A-z]{2,6}"
        self.url_s = r"^([A-z0-9]+:\/\/)?(www.|[A-z0-9].)[A-z0-9\-\.]+\.[A-z]{2,6}(\:[0-9]{1,5})*(\/($|[A-z0-9\.\,\;\?\'\\\+&amp;%\$#\=~_\-]+))*$"
        self.url_m = r"ftp|https?:\/\/[A-z0-9\-]{2,255}\.[A-z]{2,6}[\/A-z0-9\.\,\;\?\'\\\+&amp;%\$#\=~_\-]+"
        self.ipv4_s = r"^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$"
        self.ipv4_m = r"(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])"
        self.id_s = r"^@[A-z_0-9\.\-]{2,255}$"
        self.id_m = r"@[A-z_0-9\.\-]{2,255}"
        self.social_network_ulinks = {
            "instagram": r"https?:\/\/[w.]{4}?(instagram\.com\/[A-z_0-9.\-]{1,30})",
            "facebook": r"https?:\/\/[w.]{4}?(facebook\.com\/[A-z_0-9\-]{2,50})",
            "twitter": r"https?:\/\/[w.]{4}?(twitter\.com\/[A-z_0-9\-.]{2,40})",
            "github": r"https?:\/\/[w.]{4}?(github\.com\/[A-z_0-9]{1,39})",
            "telegram": r"https?:\/\/[w.]{4}?(telegram\.me/[A-z_0-9]{5,32})",
            "youtube": r"https?:\/\/[w.]{4}?(youtube\.com\/user\/[A-z_0-9\-\.]{2,100})",
            "linkedin company": r"https?:\/\/[w.]{4}?(linkedin\.com\/company\/[A-z_0-9\.\-]{3,50})",
            "linkedin individual": r"https?:\/\/[w.]{4}?(linkedin\.com\/in\/[A-z_0-9\.\-]{3,50})",
            "googleplus": r"\.?(plus\.google\.com/[A-z0-9_\-.+]{3,255})"}

    def search(self, string, regex, _type=list):
        res = [] if _type is list else False
        regex = re.findall(regex, string)
        if(regex != []):
            if(_type is bool):
                return True
            for i in regex:
                if(isinstance(i, tuple)):
                    i = "".join(i)
                    if i not in res:
                        res.append(i)
                else:
                    if i not in res:
                        res.append(i)
        else:
            return None

    def sub(self, regex, sub_string, string):
        data = re.sub(regex, sub_string, str(string))
        return data

    def is_email(self, string):
        return self.search(string, self.email_s, _type=bool)

    def is_id(self, string):
        return self.search(string, self.id_s, _type=bool)

    def is_protocol(self, string):
        return self.search(string, self.protocol_s, _type=bool)

    def is_phone(self, string):
        return self.search(string, self.phone_s, _type=bool)

    def is_domain(self, string):
        return self.search(string, self.domain_s, _type=bool)

    def is_url(self, string):
        return self.search(string, self.url_s, _type=bool)

    def is_ipv4(self, string):
        return self.search(string, self.ipv4_s, _type=bool)

    def get_emails(self, string):
        return self.search(string, self.email_m, _type=list)

    def get_ipv4(self, string):
        return self.search(string, self.ipv4_m, _type=list)

    def get_domains(self, string):
        return self.search(string, self.domain_m, _type=list)

    def get_urls(self, string):
        return self.search(string, self.url_m, _type=list)

    def get_phones(self, string):
        return self.search(string, self.phone_m, _type=list)

    def get_id(self, string):
        return self.search(string, self.id_m, _type=list)
