#!/usr/bin/python3
# -*- coding: utf-8 -*-

# version.py file is part of slpkg.

# Copyright 2014-2020 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://gitlab.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from slpkg.__metadata__ import MetaData as _meta_


def prog_version():
    """Print version, license and email
    """
    print("Version   : {0}\n"
          "Licence   : {1}\n"
          "Email     : {2}\n"
          "Homepage  : {3}\n"
          "Twitter   : {4}\n"
          "Maintainer: {5}".format(_meta_.__version__,
                                   _meta_.__license__,
                                   _meta_.__email__,
                                   _meta_.__homepage__,
                                   _meta_.__twitter__,
                                   _meta_.__maintainer__))
