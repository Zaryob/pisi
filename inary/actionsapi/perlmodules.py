# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 - 2018, Suleyman POYRAZ (Zaryob)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# standard python modules
import os
import glob

import gettext
__trans = gettext.translation('inary', fallback=True)
_ = __trans.gettext

# Inary Modules
import inary.context as ctx

# ActionsAPI Modules
import inary.actionsapi
import inary.actionsapi.get as get
from inary.actionsapi.shelltools import system
from inary.actionsapi.shelltools import can_access_file
from inary.actionsapi.shelltools import export
from inary.actionsapi.shelltools import unlink
from inary.actionsapi.shelltools import unlinkDir

class ConfigureError(inary.actionsapi.Error):
    def __init__(self, value=''):
        inary.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

class MakeError(inary.actionsapi.Error):
    def __init__(self, value=''):
        inary.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

class InstallError(inary.actionsapi.Error):
    def __init__(self, value=''):
        inary.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

def configure(parameters = ''):
    '''configure source with given parameters.'''
    export('PERL_MM_USE_DEFAULT', '1')
    if can_access_file('Build.PL'):
        if system('perl Build.PL installdirs=vendor destdir={}'.format(get.installDIR())):
            raise ConfigureError(_('Configure failed.'))
    else:
        if system('perl Makefile.PL {0} PREFIX=/usr INSTALLDIRS=vendor DESTDIR={1}'.format(parameters, get.installDIR())):
            raise ConfigureError(_('Configure failed.'))

def make(parameters = ''):
    '''make source with given parameters.'''
    if can_access_file('Makefile'):
        if system('make {}'.format(parameters)):
            raise MakeError(_('Make failed.'))
    else:
        if system('perl Build {}'.format(parameters)):
            raise MakeError(_('perl build failed.'))

def install(parameters = 'install'):
    '''install source with given parameters.'''
    if can_access_file('Makefile'):
        if system('make {}'.format(parameters)):
            raise InstallError(_('Make failed.'))
    else:
        if system('perl Build install'):
            raise MakeError(_('perl install failed.'))

    removePacklist()
    removePodfiles()

def removePacklist(path = 'usr/lib/perl5/'):
    ''' cleans .packlist file from perl packages '''
    full_path = '{0}/{1}'.format(get.installDIR(), path)
    for root, dirs, files in os.walk(full_path):
        for packFile in files:
            if packFile == ".packlist":
                if can_access_file('{0}/{1}'.format(root, packFile)):
                    unlink('{0}/{1}'.format(root, packFile))
                    removeEmptydirs(root)

def removePodfiles(path = 'usr/lib/perl5/'):
    ''' cleans *.pod files from perl packages '''
    full_path = '{0}/{1}'.format(get.installDIR(), path)
    for root, dirs, files in os.walk(full_path):
        for packFile in files:
            if packFile.endswith(".pod"):
                if can_access_file('{0}/{1}'.format(root, packFile)):
                    unlink('{0}/{1}'.format(root, packFile))
                    removeEmptydirs(root)

def removeEmptydirs(d):
    ''' remove empty dirs from perl package if exists after deletion .pod and .packlist files '''
    if not os.listdir(d) and not d == get.installDIR():
        unlinkDir(d)
        d = d[:d.rfind("/")]
        removeEmptydirs(d)