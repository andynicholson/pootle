#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with translate; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from django.db import models
from django.utils.safestring import mark_safe

from pootle_app.lib.util import RelatedManager


# These are the values for the 'type' field of Submission:
#None/0 = no information
NORMAL = 1          # Interactive web editing
REVERT = 2          # Revert action on the web
SUGG_ACCEPT = 3     # Accepting a suggestion
UPLOAD = 4          # Uploading an offline file

class Submission(models.Model):
    class Meta:
        get_latest_by = "creation_time"
        db_table = 'pootle_app_submission'

    objects = RelatedManager()

    creation_time       = models.DateTimeField(db_index=True)
    translation_project = models.ForeignKey('pootle_translationproject.TranslationProject', db_index=True)
    submitter           = models.ForeignKey('pootle_profile.PootleProfile', null=True, db_index=True)
    from_suggestion     = models.OneToOneField('pootle_app.Suggestion', null=True, db_index=True)
    unit                = models.ForeignKey('pootle_store.Unit', blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    # the field in the unit that changed:
    field               = models.CharField(max_length=128, blank=True, default=u"")
    # how did this submission come about? (one of the constants above)
    type                = models.IntegerField(null=True, blank=True, db_index=True)
    # old_value and new_value can store string representations of multistrings
    # in the case where they store values for a unit's source or target. In
    # such cases, the strings might not be usable as is. Use the two helper
    # functions in pootle_store.fields to convert to and from this format.
    old_value           = models.TextField(blank=True, default=u"")
    new_value           = models.TextField(blank=True, default=u"")

    def __unicode__(self):
        return u"%s (%s)" % (self.creation_time.strftime("%Y-%m-%d %H:%M"),
                             unicode(self.submitter))

    def as_html(self):
        snippet = u'%(time)s (<a href="%(profile_url)s">%(submitter)s</a>)' % {
                    'time': self.creation_time.strftime("%Y-%m-%d %H:%M"),
                    'profile_url': self.submitter.get_absolute_url(),
                    'submitter': unicode(self.submitter),
                }

        return mark_safe(snippet)
