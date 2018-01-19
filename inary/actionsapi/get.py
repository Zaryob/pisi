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

# Standart Python Modules
import os
import sys

import gettext
__trans = gettext.translation('inary', fallback=True)
_ = __trans.gettext

# INARY Modules
import inary.actionsapi
import inary.context as ctx

# ActionsAPI Modules
import inary.actionsapi.variables

class BinutilsError(inary.actionsapi.Error):
    def __init__(self, value=''):
        inary.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

# Globals
env = inary.actionsapi.variables.glb.env
dirs = inary.actionsapi.variables.glb.dirs
generals = inary.actionsapi.variables.glb.generals

def curDIR():
    '''returns current work directory's path'''
    return os.getcwd()

def curKERNEL():
    '''returns currently running kernel's version'''
    return os.uname()[2]

def curPYTHON():
    ''' returns currently used python's version'''
    (a, b, c, x, y) = sys.version_info
    return 'python{0}.{1}'.format(a, b)

def curPERL():
    ''' returns currently used perl's version'''
    return os.path.realpath('/usr/bin/perl').split('perl')[1]

def ENV(environ):
    '''returns any given environ variable'''
    try:
        return os.environ[environ];
    except KeyError:
        return None

# PİSİ Related Functions

def pkgDIR():
    '''returns the path of binary packages'''
    '''Default: /var/cache/inary/packages'''
    return env.pkg_dir

def workDIR():
    return env.work_dir

def installDIR():
    '''returns the path of binary packages'''
    return env.install_dir

# Pardus Related Functions

def lsbINFO():
    """Returns a dictionary filled through /etc/lsb-release."""
    return dict([(l.split("=")[0], l.split("=")[1].strip("'\"")) \
                for l in open("/etc/lsb-release", "r").read().strip().split("\n") if "=" in l])

# PSPEC Related Functions

def srcNAME():
    return env.src_name

def srcVERSION():
    return env.src_version

def srcRELEASE():
    return env.src_release

def srcTAG():
    return '{0}-{1}-{2}'.format(env.src_name, env.src_version, env.src_release)

def srcDIR():
    return '{0}-{1}'.format(env.src_name, env.src_version)

# Build Related Functions

def ARCH():
    return generals.architecture

def HOST():
    return env.host

def CHOST():
    # FIXME: Currently it behave same as HOST,
    # but will be used for cross-compiling when inary ready...
    return env.host

def CFLAGS():
    return env.cflags

def CXXFLAGS():
    return env.cxxflags

def LDFLAGS():
    return env.ldflags

def makeJOBS():
    return env.jobs

def buildTYPE():
    '''returns the current build type'''
    return env.build_type

# Directory Related Functions

def docDIR():
    return dirs.doc

def sbinDIR():
    return dirs.sbin

def infoDIR():
    return dirs.info

def manDIR():
    return dirs.man

def dataDIR():
    return dirs.data

def confDIR():
    return dirs.conf

def localstateDIR():
    return dirs.localstate

def libexecDIR():
    return dirs.libexec

def defaultprefixDIR():
    return dirs.defaultprefix

def emul32prefixDIR():
    return dirs.emul32prefix

def kdeDIR():
    return dirs.kde

def qtDIR():
    return dirs.qt

# Binutils Variables

def existBinary(bin):
    # determine if path has binary
    path = os.environ['PATH'].split(':')
    for directory in path:
        if os.path.exists(os.path.join(directory, bin)):
            return True
    return False

def getBinutilsInfo(util):
    cross_build_name = '{0}-{1}'.format(HOST(), util)
    if not existBinary(cross_build_name):
        if not existBinary(util):
            raise BinutilsError(_('Util {} cannot be found').format(util))
        else:
            ctx.ui.debug(_('Warning: {0} does not exist, using plain name {1}').format(cross_build_name, util))
            return util
    else:
        return cross_build_name

def AR():
    return getBinutilsInfo('ar')

def AS():
    return getBinutilsInfo('as')

def CC():
    return getBinutilsInfo('gcc')

def CXX():
    return getBinutilsInfo('g++')

def LD():
    return getBinutilsInfo('ld')

def NM():
    return getBinutilsInfo('nm')

def RANLIB():
    return getBinutilsInfo('ranlib')

def F77():
    return getBinutilsInfo('g77')

def GCJ():
    return getBinutilsInfo('gcj')
