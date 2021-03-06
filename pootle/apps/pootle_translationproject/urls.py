#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Zuza Software Foundation
#
# This file is part of Pootle.
#
# Pootle is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pootle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pootle; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from django.conf.urls.defaults import *
urlpatterns = patterns('pootle_translationproject.views',
    # Admin views
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/((.*/)*)admin_permissions.html$',
     'tp_admin_permissions'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/((.*/)*)admin_files.html$',
     'tp_admin_files'),

    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>(.*/)*)(index.html)?$',
     'tp_overview'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>.*)edit.html$',
     'tp_translate'),

    # XHR views
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/((.*/)*)edit_settings.html$',
     'tp_settings_edit'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>(.*/)*)dir_summary.html$',
     'tp_dir_summary'),

    # Exporting files
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<file_path>.*)export/zip$',
     'export_zip'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/translate.html$',
     'translate'),
)
