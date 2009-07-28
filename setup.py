#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, glob
import subprocess
from stat import *
from distutils.core import setup
from distutils.command.install import install as _install
from distutils.command.install_data import install_data as _install_data

INSTALLED_FILES = "installed_files"

class install(_install):

    def run(self):
        _install.run(self)
        outputs = self.get_outputs()
        length = 0
        if self.root:
            length += len(self.root)
        if self.prefix:
            length += len(self.prefix)
        if length:
            for counter in xrange(len(outputs)):
                outputs[counter] = outputs[counter][length:]
        data = "\n".join(outputs)
        try:
            file = open(INSTALLED_FILES, "w")
        except:
            self.warn("Could not write installed files list %s" % \
                       INSTALLED_FILES)
            return 
        file.write(data)
        file.close()

class install_data(_install_data):

    def run(self):
        def chmod_data_file(file):
            try:
                os.chmod(file, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)
            except:
                self.warn("Could not chmod data file %s" % file)
        _install_data.run(self)
        map(chmod_data_file, self.get_outputs())

class uninstall(_install):

    def run(self):
        try:
            file = open(INSTALLED_FILES, "r")
        except:
            self.warn("Could not read installed files list %s" % \
                       INSTALLED_FILES)
            return 
        files = file.readlines()
        file.close()
        prepend = ""
        if self.root:
            prepend += self.root
        if self.prefix:
            prepend += self.prefix
        if len(prepend):
            for counter in xrange(len(files)):
                files[counter] = prepend + files[counter].rstrip()
        for file in files:
            print "Uninstalling %s" % file
            try:
                os.unlink(file)
            except:
                self.warn("Could not remove file %s" % file)

ops = ("install", "build", "sdist", "uninstall", "clean")

if len(sys.argv) < 2 or sys.argv[1] not in ops:
    raise SystemExit("Please specify operation : " + " | ".join(ops))

prefix = None
if len(sys.argv) > 2:
    i = 0
    for o in sys.argv:
        if o.startswith("--prefix"):
            if o == "--prefix":
                if len(sys.argv) >= i:
                    prefix = sys.argv[i + 1]
                sys.argv.remove(prefix)
            elif o.startswith("--prefix=") and len(o[9:]):
                prefix = o[9:]
            sys.argv.remove(o)
            break
        i += 1
if not prefix and "PREFIX" in os.environ:
    prefix = os.environ["PREFIX"]
if not prefix or not len(prefix):
    prefix = "/usr/local"

if sys.argv[1] in ("install", "uninstall") and len(prefix):
    sys.argv += ["--prefix", prefix]

with open("VERSION") as version_file:
    version = version_file.read().strip()
    if "=" in version:
        version = version.split("=")[1]

with open(os.path.join("WallSlasher/Constants.py.in")) as f:
    data = f.read()

data = data.replace("@prefix@", prefix)
data = data.replace("@version@", version)

with open(os.path.join("WallSlasher/Constants.py"), "w") as f:
    f.write(data)

data_files = [('share/wall-slasher/glade', ['glade/wall-slasher.glade',]),
           ('/usr/share/dbus-1/system-services', ['policykit/com.kissuki.wall-slasher.service',]),
           ('/usr/share/PolicyKit/policy', ['policykit/com.kissuki.wall-slasher.policy',]),
           ('/etc/dbus-1/system.d', ['policykit/com.kissuki.wall-slasher.conf',]),
           ]

setup (
        name             = "Wall Slasher",
        version          = version,
        description      = "Wall Slasher 是一个对类 Unix 系统的 hosts 文件的简单管理工具，用于屏蔽广告和修复一些网站复杂的网络问题。",
        author           = "Iven Day (Xu Lijian)",
        author_email     = "ivenvd@gmail.com",
        url              = "http://www.kissuki.com/",
        license          = "GPL",
        data_files       = data_files,
        packages         = ["WallSlasher"],
        scripts          = ["wall-slasher"],
        cmdclass         = {"uninstall" : uninstall,
                            "install" : install,
                            "install_data" : install_data}
     )

os.remove ("WallSlasher/Constants.py")
