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

import gettext

__trans = gettext.translation('inary', fallback=True)
_ = __trans.gettext

import inary.db
import inary.cli.command as command
from inary.operations import repository


class EnableRepo(command.Command, metaclass=command.autocommand):
    __doc__ = _("""Enable repository

Usage: enable-repo [<repo1> <repo2> ... <repon>]

<repoi>: repository name

Disabled repositories are not taken into account in operations
""")

    def __init__(self, args):
        super(EnableRepo, self).__init__(args)
        self.repodb = inary.db.repodb.RepoDB()

    name = (_("enable-repo"), "er")

    def run(self):
        self.init(database=True)

        if not self.args:
            self.help()
            return

        for repo in self.args:
            if self.repodb.has_repo(repo):
                repository.set_repo_activity(repo, True)
