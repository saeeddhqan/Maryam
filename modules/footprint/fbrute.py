# -*- coding : u8 -*-
"""
OWASP Maryam!

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

from core.module import BaseModule
import re

class Module(BaseModule):

	meta = {
		"name": "File and Directory Brute Force",
		"author": "Saeeddqn",
		"version": "0.5",
		"description": "Search hosts for interesting files in predictable locations and brute force it.",
		"options": (
			("domain", BaseModule._global_options["target"], True, "Domain string", "-d", "store"),
			("logs", True, False, "Log files search(with 7 payload)", "--logs", "store_true"),
			("backup", True, False, "Backup files search(with 148 payload)", "--backup", "store_true"),
			("apache", True, False, "Apache status check(with 5 payload", "--apache", "store_true"),
			("admin", True, False, "Admin panel check(with 482 payload)", "--admin", "store_true"),
			("wordlist", None, False, "Payload address file for url brute force attack(with \\n separator)", "-w", "store"),
			("output", False, False, "Save output to workspace", "--output", "store_true"),
		),
		"examples": ["fbrute -d <DOMAIN> --log --admin -w <WORDLIST>", "fbrute -d <DOMAIN> --backup --apache --admin --output"]
	}

	def module_run(self):
		url = self.urlib(self.options["domain"]).sub_service("http")
		resp = {}
		methods = []
		
		### General Files ####
		######################
		resp["general"] = []
		gens = {
			"web-console": "Administration",
			"elmah.axd": "Error Log fo",
			"sitemap.xml": "<?xml",
			"sitemap.xml.gz": "<?xml",
			"robots.txt": "User-agent:",
			"server-status": ">Apache Status<",
			"jmx-console": "JBoss",
			"admin-console": "index.seam"}
			
		php_info_list = ["INSTALL.php?mode=phpinfo", "PhpInfo.php", "PHPinfo.php", "phpinfo.php", "PHPINFO.php", "phpInfo.php", "info.php", "Info.php", "INFO.php", "test.php?mode=phpinfo", "index.php?view=phpinfo", "index.php?mode=phpinfo", "TEST.php?mode=phpinfo", "?mode=phpinfo", "?view=phpinfo",
						 "install.php?mode=phpinfo", "admin.php?mode=phpinfo", "phpversion.php", "phpVersion.php", "test1.php", "test.php", "test2.php",
						 "phpinfo1.php", "phpInfo1.php", "info1.php", "PHPversion.php", "test", "php", "a.php", "x.php", "xx.php", "xxx.php"]

		self.heading("General mode:", level=0)
		for i in gens:
			urjoin = self.urlib(url).join(i)
			try:
				req = self.request(urjoin)
			except Exception as e:
				pass
			else:
				if gens[i] in req.text and req.status_code == 200:
					resp["general"].append(urjoin)
					self.output("\t\"%s\" > found" % urjoin, "g")
				else:
					self.output("\t\"%s\" > not found" % urjoin)

		# phpinfo
		self.heading("phpinfo file:", level=0)
		for i in php_info_list:
			urjoin = self.urlib(url).join(i)
			try:
				req = self.request(urjoin)
			except Exception as e:
				print(e.message)
			else:
				cond1 = re.search(r"<title>phpinfo()</title>|<h1 class=\"p\">PHP Version|<h2><a name=\"module_apache2handler\">apache2handler</a></h2>", req.text)
				cond2 = req.status_code == 200
				if cond1 and cond2:
					self.output("\t\"%s\" > found" % urjoin, "g")
					resp["phpinfo"].append(urjoin)

		### LOGS File Brute Force ####
		##############################
		if self.options["logs"]:
			methods.append("logs")
			resp["logs"] = []
			paths = ["error_log", "error.log", "debug.log", "php.errors",
					 "php5-fpm.log", "php_errors.log", "security.txt"]

			self.heading("log files:", level=0)
			for i in paths:
				urjoin = self.urlib(url).join(i)
				try:
					req = self.request(urjoin)
				except Exception:
					pass
				else:
					cond1 = False
					if "Content-Type" in req.headers:
						cond1 = req.headers["Content-Type"] == "text/plain"
					cond2 = req.status_code == 200
					if cond1 and cond2:
						resp["logs"].append(urjoin)
						self.output("\t\"%s\" > found" % urjoin, "g")
					else:
						self.output("\t\"%s\" > not found" % urjoin)

		## BACKUP Brute Force ##
		########################
		if self.options["backup"]:
			methods.append("logs")
			resp["logs"] = []
			paths = ["1.txt", "2.txt", "1.gz", "1.rar", "1.save", "1.tar", "1.tar.bz2", "1.tar.gz", "1.tgz", "1.tmp", "1.zip", "2.back", "2.backup", "2.gz", "2.rar", "2.save", "2.tar", "2.tar.bz2", "2.tar.gz", "2.tgz", "2.tmp", "2.zip", "backup.back", "backup.backup", "backup.bak", "backup.bck", "backup.bkp", "backup.copy", "backup.gz", "backup.old", "backup.orig", "backup.rar", "backup.sav", "backup.save", "backup.sql.back", "backup.sql.backup", "backup.sql.bak", "backup.sql.bck", "backup.sql.bkp", "backup.sql.copy", "backup.sql.gz", "backup.sql.old", "backup.sql.orig", "backup.sql.rar", "backup.sql.sav", "backup.sql.save", "backup.sql.tar", "backup.sql.tar.bz2", "backup.sql.tar.gz", "backup.sql.tgz", "backup.sql.tmp", "backup.sql.txt", "backup.sql.zip", "backup.tar", "backup.tar.bz2", "backup.tar.gz", "backup.tgz", "backup.txt", "backup.zip", "database.back", "database.backup", "database.bak", "database.bck", "database.bkp", "database.copy", "database.gz", "database.old", "database.orig", "database.rar", "database.sav", "database.save", "database.sql~", "database.sql.back", "database.sql.backup", "database.sql.bak",
					 "database.sql.bck", "database.sql.bkp", "~backup", "backup", "database.sql.copy", "database.sql.gz", "database.sql.old", "database.sql.orig", "database.sql.rar", "database.sql.sav", "database.sql.save", "database.sql.tar", "database.sql.tar.bz2", "database.sql.tar.gz", "database.sql.tgz", "database.sql.tmp", "database.sql.txt", "database.sql.zip", "database.tar", "database.tar.bz2", "database.tar.gz", "database.tgz", "database.tmp", "database.txt", "database.zip", "site.back", "site.backup", "site.bak", "site.bck", "site.bkp", "site.copy", "site.gz", "site.old", "site.orig", "site.rar", "site.sav", "site.save", "site.tar", "site.tar.bz2", "site.tar.gz", "site.tgz", "site.zip", "sql.zip.back", "sql.zip.backup", "sql.zip.bak", "sql.zip.bck", "sql.zip.bkp", "sql.zip.copy", "sql.zip.gz", "sql.zip.old", "sql.zip.orig", "sql.zip.save", "sql.zip.tar", "sql.zip.tar.bz2", "sql.zip.tar.gz", "sql.zip.tgz", "upload.back", "upload.backup", "upload.bak", "upload.bck", "upload.bkp", "upload.copy", "upload.gz", "upload.old", "upload.orig", "upload.rar", "upload.sav", "upload.save", "upload.tar", "upload.tar.bz2", "upload.tar.gz", "upload.tgz", "upload.zip"]

			self.heading("Backup files:", level=0)
			for i in paths:
				urjoin = self.urlib(url).join(i)
				try:
					req = self.request(urjoin)
				except Exception:
					pass
				else:
					cond1 = False
					if "Content-Type" in req.headers:
						cond1 = req.headers["Content-Type"] == "text/plain"
					cond2 = req.status_code == 200
					if cond1 and cond2:
						resp["logs"].append(urjoin)
						self.output("\t\"%s\" > found" % urjoin, "g")
					else:
						self.output("\t\"%s\" > not found" % urjoin)

		## APACHE Brute Force ##
		########################
		if self.options["apache"]:
			methods.append("apache")
			resp["apache"] = []
			paths = ["perl-status", "server-status", "server-info",
					 "stronghold-info", "stronghold-status"]

			self.heading("Apache Status:", level=0)
			for i in paths:
				urjoin = self.urlib(url).join(i)
				try:
					req = self.request(urjoin)
				except Exception:
					pass
				else:
					cond = req.status_code == 200
					if cond:
						resp["apache"].append(urjoin)
						self.output("\t\"%s\" > found" % urjoin, "g")
					else:
						self.output("\t\"%s\" > not found" % urjoin)

		## ADMIN Brute Force ###
		########################
		if self.options["admin"]:
			methods.append("admin")
			resp["admin"] = []
			paths = ["~adm", "~admin", "~administrator", "~amanda", "~apache", "~bin", "~ftp", "~guest", "~http", "~httpd", "~log", "~logs", "~lp", "~mail", "~nobody", "~operator", "~root", "~sys", "~sysadm", "~sysadmin", "~test", "~tmp", "~user", "~webmaster", "~www", "wp-admin", "wp-login.php", "administrator", "database.sql", "backup-db", "mysql.sql", "phpmyadmin", "server-status", "server-info", "php.php", "test.php", ".git", ".htaccess", ".htaccess.old", ".htaccess.save", ".htaccess.txt", ".php-ini", "php-ini", "FCKeditor", "FCK", "editor", "Desktop.ini", "INSTALL", "install", "install.php", "update", "upgrade", "upgrade.php", "update.php", "LICENSE", "LICENSE.txt", "Server.php", "WS_FTP.LOG", "WS_FTP.ini", "WS_FTP.log", "Web.config", "Webalizer", "webalizer", "config.php", "config.php.new", "config.php~", "controlpanel", "cpanel", "favicon.ico", "old", "php-error", "php.ini~", "php.ini", "php.log", "robots.txt", "security", "webdav", "1", "acceso.asp", "acceso.php", "access", "access.php", "account", "account.asp", "account.html", "account.php", "acct_login", "_adm_", "_adm", "adm", "adm2", "adm/admloginuser.asp", "adm/admloginuser.php", "adm.asp", "adm_auth.asp", "adm_auth.php", "adm.html", "_admin_", "_admin", "admin1", "admin1.asp", "admin1.html", "admin1.php", "admin2", "admin2.asp", "admin2.html", "admin2/index", "admin2/index.asp", "admin2/index.php", "admin2/login.asp", "admin2/login.php", "admin2.php", "admin3", "admin4", "admin4_account", "admin4_colon", "admin5", "admin/account.asp", "admin/account.html", "admin/account.php", "admin/add_banner.php", "addblog.php", "admin/add_gallery_image.php", "admin/add.php", "admin/add", "room.php", "slider.php", "add_testimonials.php", "admin/admin", "admin/adminarea.php", "admin/admin.asp", "admin/AdminDashboard.php", "home.php", "admin/AdminHome.php", "admin/admin.html", "admin/admin_index.php", "admin/admin_login.asp", "login.asp", "admin/adminLogin.asp", "admin/admin_login.html", "login.html", "admin/adminLogin.html", "admin/admin_login.php", "adminLogin.php", "admin/admin_management.php", "admin/admin.php", "admin/admin_users.php", "admin/adminview.php", "admin/adm.php", "admin_area", "adminarea", "admin_area/admin.asp", "adminarea/admin.asp", "admin_area/admin.html", "adminarea/admin.html", "admin.php", "adminarea/admin.php", "admin_area/index.asp", "adminarea/index.asp", "admin_area/index.html", "adminarea/index.html", "admin_area/index.php", "adminarea/index.php", "admin_area/login.asp", "adminarea/login.asp", "admin_area/login.html", "adminarea/login.html", "admin_area/login.php", "adminarea/login.php", "admin.asp", "admin/banner.php", "admin/banners_report.php", "admin/category.php", "change_gallery.php", "admin/checklogin.php", "admin/configration.php", "admincontrol.asp", "admincontrol.html", "admincontrol/login.asp", "admincontrol/login.html", "admincontrol/login.php", "admin/control_pages/admin_home.php", "admin/controlpanel.asp", "admin/controlpanel.html", "admin/controlpanel.php", "admincontrol.php", "admin/cpanel.php", "admin/cp.asp", "admin/CPhome.php", "admin/cp.html", "admincp/index.asp", "admincp/index.html", "admincp/login.asp", "admin/cp.php", "admin/dashboard/index.php", "admin/dashboard.php", "admin/dashbord.php", "admin/dash.php", "admin/default.php", "adm/index.asp", "adm/index.html", "adm/index.php", "admin/enter.php", "admin/event.php", "admin/form.php", "admin/gallery.php", "admin/headline.php", "admin/home.asp", "admin/home.html", "admin_home.php", "admin/home.php", "admin.html", "admin/index.asp", "admin/index", "digital.php", "index.html", "admin/index.php", "admin/index_ref.php", "admin/initialadmin.php", "administer", "administr8", "administr8.asp", "administr8.html", "administr8.php", "administracion.php", "administrador", "administratie", "administration", "administration.html", "administration.php", "_administrator_", "_administrator", "administrator/account.asp", "administrator/account.html", "administrator/account.php", "administratoraccounts", "administrator.asp", "administrator.html", "administrator/index.asp", "administrator/index.html",
					"administratorlogin", "administrator/login.asp", "administratorlogin.asp", "administrator/login.html", "administrator/login.php", "administratorlogin.php", "administrator.php", "administrators", "administrivia", "leads.php", "admin/list_gallery.php", "admin/login", "adminLogin", "admin_login.asp", "admin/login.asp", "adminLogin.asp", "admin_login.html", "admin/login.html", "adminLogin.html", "ADMIN/login.html", "admin_login.php", "login.php ", "admin", "admin/login.php", "ADMIN/login.php", "admin/login_success.php", "admin/loginsuccess.php", "admin/log.php", "admin_main.html", "admin/main_page.php", "admin/main.php", "ManageAdmin.php", "admin/manageImages.php", "admin/manage_team.php", "admin/member_home.php", "admin/moderator.php", "admin/my_account.php", "admin/myaccount.php", "admin/overview.php", "admin/page_management.php", "admin/pages/home_admin.php", "adminpanel", "adminpanel.asp", "adminpanel.html", "adminpanel.php", "Admin/private", "adminpro", "admin/product.php", "admin/products.php", "admins", "admins.asp", "admin/save.php", "admins.html", "admin/slider.php", "admin/specializations.php", "admins.php", "admin_tool", "AdminTools", "admin/uhome.html", "admin/upload.php", "admin/userpage.php", "admin/viewblog.php", "admin/viewmembers.php", "admin/voucher.php", "AdminWeb", "admin/welcomepage.php", "admin/welcome.php", "admloginuser.asp", "admloginuser.php", "admon", "ADMON", "adm.php", "affiliate.asp", "affiliate.php", "auth", "auth/login", "authorize.php", "autologin", "banneradmin", "base/admin", "bb", "bbadmin", "admin/admin.html /bb", "admin/admin.php /bb", "admin/index.asp /bb", "admin/index.html /bb", "admin/index.php /bb", "admin/login.asp /bb", "admin/login.html /bb", "bigadmin", "blogindex", "cadmins", "ccms", "ccms/login.php", "ccp14admin", "cms", "cms/admin", "cmsadmin", "cms/_admin/logon.php", "cms/login", "configuration", "configure", "controlpanel.asp", "controlpanel.html", "controlpanel.php", "cPanel", "cpanel_file", "cp.asp", "cp.html", "cp.php", "customer_login",
					"database_administration", "Database_Administration", "db/admin.php", "directadmin", "dir", "edit.php", "evmsadmin", "ezsqliteadmin", "fileadmin", "fileadmin.asp", "fileadmin.html", "fileadmin.php", "formslogin", "forum/admin", "globes_admin", "home.asp", "home.html", "hpwebjetadmin", "include/admin.php", "includes/login.php", "Indy_admin", "instadmin", "interactive/admin.php", "irc", "links/login.php", "LiveUser_Admin", "login", "login1", "login_db", "loginflat", "login/login.php", "login.php", "redirect", "logins", "us", "logon", "logo_sysadmin", "Lotus_Domino_Admin", "mag/admin", "maintenance", "manage_admin.php", "manager", "manager/ispmgr", "manuallogin", "memberadmin", "memberadmin.asp", "memberadmin.php", "members", "memlogin", "meta_login", "modelsearch", "modelsearch/admin.html", "modelsearch/admin.php", "modelsearch/index.asp", "modelsearch/index.html", "index.php", "modelsearch/login.asp", "modelsearch/login.html", "modelsearch/login.php", "moderator", "moderator/admin.asp", "moderator/admin.html", "moderator/admin.php", "moderator.asp", "moderator.html", "moderator/login.asp", "moderator/login.html", "moderator/login.php", "moderator.php", "myadmin", "navSiteAdmin", "newsadmin", "nsw/admin/login.php", "openvpnadmin", "pages/admin/admin", "login.php /panel", "panel", "administracion/admin.asp", "administracion/admin.html", "paneldecontrol", "panel.php", "pgadmin", "phpldapadmin", "phppgadmin", "phpSQLiteAdmin", "platz_login", "pma", "power_user", "project", "pureadmin", "radmind", "rcLogin", "server", "ServerAdministrator", "server_admin_small", "Server.asp", "Server.html", "showlogin", "simpleLogin", "site/admin", "siteadmin", "siteadmin/index.asp", "siteadmin/index.php", "siteadmin/login.asp", "siteadmin/login.html", "site_admin/login.php", "siteadmin/login.php", "smblogin", "sql", "sshadmin", "ss_vms_admin_sm", "staradmin", "sub", "sysadmins", "system_administration", "system", "user.html", "utility_login", "vadmind", "vmailadmin", "webadmin/admin.html", "webadmin/admin.php", "webadmin.asp", "webadmin.html", "webadmin/index.asp", "webadmin/index.html", "webadmin/index.php", "webadmin/login.asp", "webadmin/login.html", "webadmin/login.php", "webadmin.php"]

			self.heading("Admin panel:", level=0)
			for i in paths:
				urjoin = self.urlib(url).join(i)
				try:
					req = self.request(urjoin)
				except Exception:
					continue
				else:
					cond = req.status_code in [200, 401, 403]
					if cond:
						resp["admin"].append(urjoin)
						self.output("\t\"%s\" > found" % urjoin, "g")

		### URL Brute Force ####
		########################
		if self.options["wordlist"]:
			methods.append("brute")
			resp["brute"] = []
			max_attempt = 4
			attempt = 0
			filename = self.options["wordlist"]

			try:
				with open(filename) as o:
					read = o.read().split()
			except IOError as e:
				self.error("IOError: %s"% e.args[1])
				return

			self.heading("File Brute Force", level=0)
			for i in read:
				if attempt > max_attempt:
					break
				tmp_name = self.urlib(url).join(i)
				try:
					req = self.request(tmp_name)
				except Exception as e:
					if e.args[0] == "timed out":
						self.verbose("%s => Timed out" % tmp_name, "O")
						attempt += 1
					else:
						self.verbose("%s:\"%s\"" % (e.args[0], tmp_name), "O")
				else:
					resp["brute"].append("tmp_name")
					self.output("\"%s\"" % tmp_name, "G")

		self.save_gather(resp, "footprint/fbrute", url, output=self.options["output"])
