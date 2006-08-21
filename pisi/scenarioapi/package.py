#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# Authors:  Faik Uygur <faik@pardus.org.tr>

import os
import glob

from pisi.scenarioapi.pspec import Pspec
from pisi.scenarioapi.actions import Actions
from pisi.scenarioapi.constants import *
from pisi.scenarioapi.withops import *

class Package:
    def __init__(self, name, deps = [], cons = [], date = "2006-18-18", ver = "1.0"):
        self.name = name
        self.dependencies = deps
        self.conflicts = cons
        self.version = ver
        self.date = date
        self.pspec = None
        self.actions = None
        self.create_package()

    def create_pisi(self):
        os.system("pisi build %s -O %s > /dev/null 2>&1" % (consts.pspec_path, consts.repo_path))

    def create_package(self):
        pspec = Pspec(self.name, consts.pspec_path)
        pspec.set_source(consts.homepage, consts.summary % self.name, consts.description % self.name, consts.license)
        pspec.set_packager(consts.packager_name, consts.packager_email)
        pspec.set_archive(consts.skel_sha1sum, consts.skel_type, consts.skel_uri)
        pspec.set_package(self.dependencies, self.conflicts)
        pspec.add_file_path(consts.skel_bindir, consts.skel_dirtype)
        pspec.set_history(self.date, self.version)

        actions = Actions(self.name, consts.actionspy_path)

        self.pspec = pspec
        self.actions = actions
        self.pspec.write()
        self.actions.write()

        self.create_pisi()

    def get_file_name(self):
        # use glob. there may be buildnos at the end of the package name
        pkg = glob.glob(consts.repo_path + 
                        self.name + "-" +
                        self.version + "-" + 
                        self.pspec.pspec.history[0].release +
                        consts.glob_pisis)[0]

        return os.path.basename(pkg)
        
    def version_bump(self, *args):
        if args:
            for with in args:
                if with.types == CONFLICT and with.action == ADDED:
                    self.pspec.add_conflicts(with.pkgs)

                if with.types == CONFLICT and with.action == REMOVED:
                    self.pspec.remove_conflicts(with.pkgs)

                if with.types == DEPENDENCY and with.action == ADDED:
                    self.pspec.add_dependencies(with.pkgs)

                if with.types == DEPENDENCY and with.action == REMOVED:
                    self.pspec.remove_dependencies(with.pkgs)

        self.pspec.update_history(self.date, self.version)
        self.actions.name = self.name
        self.actions.write()
        self.create_pisi()

if __name__ == "__main__":
    p = Package("w0rmux", [], [], "0.7")
    p.version_bump()
    
