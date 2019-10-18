# -*- coding: u8 -*-
# Based on the Recon-ng: https://github.com/lanmaster53/recon-ng
from __future__ import print_function
__version__ = "v1.3.2"
import errno
import imp
import os
import random
import re
import shutil
import sys

# import framework libs
from core import framework

# using stdout to spool causes tab complete issues
# therefore, override print function
# use a lock for thread safe console and spool output
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

from threading import Lock
_print_lock = Lock()

# spooling system
def spool_print(*args, **kwargs):
    with _print_lock:
        if(framework.Framework._spool):
            framework.Framework._spool.write("%s\n" % (args[0]))
            framework.Framework._spool.flush()
        if("console" in kwargs and kwargs["console"] is False):
            return
        # new print function must still use the old print function via the
        # backup
        __builtin__._print(*args, **kwargs)


# make a builtin backup of the original print function
__builtin__._print = print
# override the builtin print function with the new print function
__builtin__.print = spool_print

# =================================================
# BASE CLASS
# =================================================

class Base(framework.Framework):

    def __init__(self):
        framework.Framework.__init__(self, "base")
        self._mode = 0
        self._config = {
                "app_name" : "maryam",
                "module_extention" : ".py",
                "data_directory_name" : "data",
                "module_directory_name" : "modules"
            }
        self._name = self._config["app_name"]
        self._prompt_template = "%s[%s] > "
        self._base_prompt = self._prompt_template % ('', self._name)
        # establish dynamic paths for framework elements
        self.app_path = framework.Framework.app_path = sys.path[0]
        self.data_path = framework.Framework.data_path = os.path.join(
            self.app_path, self._config["data_directory_name"])
        self.core_path = framework.Framework.core_path = os.path.join(
            self.app_path, "core")
        self.module_path = framework.Framework.module_path = os.path.join(
            self.app_path, self._config["module_directory_name"])
        self.module_extention = framework.Framework.module_extention = self._config[
            "module_extention"]
        self.module_dirname = framework.Framework.module_dirname = self._config[
            "module_directory_name"]
        self.options = self._global_options
        self._init_global_options()
        self._init_home()
        self.init_workspace("default")
        if self._mode == Mode.CONSOLE:
            self.show_banner()

    # ==================================================
    # SUPPORT METHODS
    # ==================================================

    def _init_global_options(self):
        self.register_option("target", "example.com", True,
                             "target for DNS interrogation")
        self.register_option("proxy", None, False,
                             "proxy server (address:port)")
        self.register_option(
            "limit", 10, True, "number of limit (where applicable)")
        self.register_option(
            "agent", "request.v0.1", True, "user-agent string")
        self.register_option("timeout", 10, True, "socket timeout (seconds)")
        self.register_option(
            "verbosity",
            '1',
            True,
            "verbosity level (0 = minimal, 1 = verbose, 2 = debug)")

    def _init_home(self):
        self._home = framework.Framework._home = os.path.expanduser('~')
        # initialize home folder
        if(not os.path.exists(self._home)):
            os.makedirs(self._home)

    def _load_modules(self):
        self.loaded_category = {}
        self._loaded_modules = framework.Framework._loaded_modules
        # crawl the module directory and build the module tree
        for path in [os.path.join(x, self.module_dirname)
                     for x in (self.app_path, self._home)]:
            for dirpath, dirnames, filenames in os.walk(path):
                # remove hidden files and directories
                filenames = [f for f in filenames if not f[0] == '.']
                dirnames[:] = [d for d in dirnames if not d[0] == '.']
                if(len(filenames) > 0):
                    for filename in [f for f in filenames if f.endswith(
                            self.module_extention)]:

                        is_loaded = self._load_module(dirpath, filename)
                        mod_category = "disabled"
                        if(is_loaded):
                            modules_reg = r'/' + \
                                self.module_dirname + r"/([^/]*)"
                            try:
                                mod_category = re.search(
                                    modules_reg, dirpath).group(1)
                            except AttributeError:
                                mod_path = os.path.join(dirpath, filename)
                                mod_category = re.search(modules_reg,
                                                         mod_path).group(1).replace(
                                    self.module_extention,
                                    '')

                        # store the resulting category statistics
                        if(mod_category not in self.loaded_category):
                            self.loaded_category[mod_category] = 0
                        self.loaded_category[mod_category] += 1

    def _load_module(self, dirpath, filename):
        mod_name = filename.split('.')[0]
        mod_dispname = '/'.join(re.split("/%s/" % self.module_dirname, dirpath)
                                [-1].split('/') + [mod_name])
        mod_loadname = mod_dispname.replace("/", "_")
        mod_loadpath = os.path.join(dirpath, filename)
        mod_file = open(mod_loadpath)
        try:
            # import the module into memory
            imp.load_source(mod_loadname, mod_loadpath, mod_file)
            __import__(mod_loadname)
            # add the module to the framework's loaded modules
            self._loaded_modules[mod_dispname] = sys.modules[mod_loadname].Module(
                mod_dispname)
            return True
        except ImportError as e:
            # notify the user of missing dependencies
            self.error("Module \'%s\' disabled. Dependency required: \'%s\'" % (
                mod_dispname, e.args[0][16:]))
        except BaseException:
            # notify the user of errors
            self.print_exception()
            self.error("Module \'%s\' disabled." % (mod_dispname))
        # remove the module from the framework's loaded modules
        self._loaded_modules.pop(mod_dispname, None)
        return False

    # ==================================================
    # WORKSPACE METHODS
    # ==================================================

    def init_workspace(self, workspace):
        workspace = os.path.join(self._home, "workspaces", workspace)
        try:
            os.makedirs(workspace)
        except OSError as e:
            if(e.errno != errno.EEXIST):
                self.error(e.__str__())
                return False
        # set workspace attributes
        self.workspace = framework.Framework.workspace = workspace
        self.prompt = self._prompt_template % (self._base_prompt[:-3], self.workspace.split('/')[-1])
        # load workspace configuration
        self._init_global_options()
        self._load_config()
        # load modules after config to populate options
        self._load_modules()
        return True

    def delete_workspace(self, workspace):
        path = os.path.join(self._home, "workspaces", workspace)
        try:
            shutil.rmtree(path)
        except OSError:
            return False
        if(workspace == self.workspace.split('/')[-1]):
            self.init_workspace("default")
        return True

    def _get_workspaces(self):
        dirnames = []
        path = os.path.join(self._home, "workspaces")
        dirnames = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
        return dirnames

    # ==================================================
    # SHOW METHODS
    # ==================================================

    def show_banner(self):
        banner = open(os.path.join(self.data_path, "banner.txt")).read()
        print(banner)
        # print version
        print(" "*15 + __version__)
        print('')
        if(self.loaded_category == {}):
            print(
                "%s[0] %s%s" %
                (framework.Colors.B,
                 "no module to display".title(),
                 framework.Colors.N))
        else:
            counts = [(self.loaded_category[x], x)
                      for x in self.loaded_category] if self.loaded_category != [] else [0]
            count_len = len(max([str(x[0]) for x in counts], key=len))
            for count in sorted(counts, reverse=True):
                cnt = "[%d]" % (count[0])
                mod_name = count[1].title() if '/' in count[1] else count[1]
                print("%s%s %s modules%s" % (framework.Colors.B, cnt.ljust(
                    count_len + 2), mod_name, framework.Colors.N))
        print('')

    def show_workspaces(self):
        self.do_workspaces('list')

    #==================================================
    # HELP METHODS
    #==================================================

    def help_workspaces(self):
        print(getattr(self, "do_workspaces").__doc__)
        print('')
        print("Usage: workspaces [add|select|delete|list]")
        print('')

    # ==================================================
    # COMMAND METHODS
    # ==================================================

    def do_reload(self, params):
        '''Reloads all modules'''
        self.output("Reloading...")
        self._load_modules()

    def do_workspaces(self, params):
        '''Manages workspaces'''
        if not params:
            self.help_workspaces()
            return
        params = params.split()
        arg = params.pop(0).lower()
        if(arg == "list"):
            header = "\nWorkspaces:\n"
            print(header + self.ruler * len(header[2:]))
            for i in self._get_workspaces():
                print(''.ljust(5) + i)
            print('')
        elif(arg in ["add", "select"]):
            if(len(params) == 1):
                if not self.init_workspace(params[0]):
                    self.output("Unable to initialize \"%s\" workspace." % (params[0]))
            else:
                print("Usage: workspace [add|select|delete] <name>")
        elif(arg == "delete"):
            if(len(params) == 1):
                if(not self.delete_workspace(params[0])):
                    self.output("Unable to delete \"%s\" workspace." % (params[0]))
            else:
                print("Usage: workspace delete <name>")
        else:
            self.help_workspaces()

    def do_load(self, params):
        '''Loads specified module'''
        try:
            self._validate_options()
        except framework.FrameworkException as e:
            self.error(e.message)
            return
        if(not params):
            self.help_load()
            return
        # finds any modules that contain params
        modules = [params] if params in self._loaded_modules else [
            x for x in self._loaded_modules if params in x]
        # notify the user if none or multiple modules are found
        if(len(modules) != 1):
            if(not modules):
                self.error("Invalid module name.")
            else:
                self.output("Multiple modules match \"%s\"." % params)
                self.show_modules(modules)
            return
        # load the module
        mod_dispname = modules[0]
        # loop to support reload logic
        while True:
            y = self._loaded_modules[mod_dispname]
            # send analytics information
            mod_loadpath = os.path.abspath(sys.modules[y.__module__].__file__)

            # return the loaded module if in command line mode
            if(self._mode == Mode.CLI):
                return y
            # begin a command loop
            y.prompt = self._prompt_template % (
                self.prompt[:-3], mod_dispname.split('/')[-1])
            try:
                y.cmdloop()

            except KeyboardInterrupt:
                print('')
            if(y._exit == 1):
                return True
            if(y._reload == 1):
                self.output("Reloading...")
                # reload the module in memory
                is_loaded = self._load_module(os.path.dirname(
                    mod_loadpath), os.path.basename(mod_loadpath))
                if(is_loaded):
                    # reload the module in the framework
                    continue
                # shuffle category counts?
            break

    do_use = do_load


# =================================================
# SUPPORT CLASSES
# =================================================
class Mode(object):
    '''Contains constants that represent the state of the interpreter.'''
    CONSOLE = 0
    CLI = 1
    GUI = 2

    def __init__(self):
        raise NotImplementedError("This class should never be instantiated.")
