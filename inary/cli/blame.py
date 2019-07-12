# -*- coding:utf-8 -*-
#
# Main fork Pisi: Copyright (C) 2005 - 2011, Tubitak/UEKAE
#
# Copyright (C)  2017 - 2018,  Suleyman POYRAZ (Zaryob)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import optparse

import gettext
__trans = gettext.translation('inary', fallback=True)
_ = __trans.gettext

import inary.cli.command as command
import inary.context as ctx
import inary.db

class Blame(command.Command, metaclass=command.autocommand):
    __doc__ = _("""Information about the package owner and release

Usage: blame <package> ... <package>

""")

    def __init__(self, args=None):
        super(Blame, self).__init__(args)
        self.installdb = inary.db.installdb.InstallDB()

    name = (_("blame"), "bl")

    def options(self):
        group = optparse.OptionGroup(self.parser, _("blame options"))
        group.add_option("-r", "--release", action="store", type="int", help=_("Blame for the given release"))
        group.add_option("-a", "--all", action="store_true", default=False,
                         help=_("Blame for all of the releases"))
        self.parser.add_option_group(group)

    def run(self):
        self.init(database=False, write=False)

        if not self.args:
            self.help()
            return

        for package in self.args:
            if self.installdb.has_package(package):
                pkg = self.installdb.get_package(package)
                release = ctx.get_option('release')
                if not release and not ctx.get_option('all'):
                    self.print_package_info(pkg)
                elif ctx.get_option('all'):
                    for hno, update in enumerate(pkg.history):
                        self.print_package_info(pkg, hno)
                else:
                    for hno, update in enumerate(pkg.history):
                        if int(update.release) == release:
                            self.print_package_info(pkg, hno)
                            return

    @staticmethod
    def print_package_info(package, hno=0):
        s = _('Name: {0}, version: {1}, release: {2}\n').format(
            package.name, package.history[hno].version, package.history[hno].release)
        s += _('Package Maintainer: {0} <{1}>\n').format(str(package.source.packager.name),
                                                         package.source.packager.email)
        s += _('Release Updater: {0.name} <{0.email}>\n').format(package.history[hno])
        s += _('Update Date: {}\n').format(package.history[hno].date)
        s += '\n{}\n'.format(package.history[hno].comment)
        ctx.ui.info(s)
