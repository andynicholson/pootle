#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009-2012 Zuza Software Foundation
#
# This file is part of Pootle.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import urlparse


def strip_trailing_slash(path):
    """If path ends with a /, strip it and return the stripped version."""
    if len(path) > 0 and path[-1] == '/':
        return path[:-1]
    else:
        return path


def url_split(path):
    try:
        slash_pos = strip_trailing_slash(path).rindex('/')
        return path[:slash_pos+1], path[slash_pos+1:]
    except ValueError:
        return '', path


def parent(url):
    parent_part, _child_part = url_split(url)
    return parent_part


def basename(url):
    _parent_part, child_part = url_split(url)
    return child_part


def ensure_uri(uri):
    """Ensure that we return a URI that the user can click on in an a tag."""
    if not uri:
        return uri
    scheme, netloc, path, query, fragment = urlparse.urlsplit(uri)
    if scheme:
        return uri

    if u'@' in uri:
        uri = u"mailto:%s" % uri
    else:
        # If we don't supply a protocol, browsers will interpret it as a
        # relative URL, like
        # http://pootle.locamotion.org/af/pootle/bugs.locamotion.org
        # So let's assume http
        uri = u"http://" + uri
    return uri
