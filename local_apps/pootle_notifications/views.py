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

from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q

from pootle.i18n.gettext import tr_lang

from pootle_app.models import Directory
from pootle_app.models.permissions import get_matching_permissions, check_permission, check_profile_permission
from pootle_app.views.language import navbar_dict
from pootle_profile.models import get_profile, PootleProfile
from pootle_notifications.models import Notice, NoticeForm
from pootle.settings import DEFAULT_FROM_EMAIL
from pootle_language.models import Language
from pootle_project.models import Project

import sys

def view(request, path):
    #FIXME: why do we have leading and trailing slashes in pootle_path?
    pootle_path = '/%s' % path

    directory = get_object_or_404(Directory, pootle_path=pootle_path)

    request.permissions = get_matching_permissions(get_profile(request.user), directory)

    if not check_permission('view', request):
        raise PermissionDenied

    template_vars = {'path': path,
                     'directory': directory}

    if check_permission('administrate', request):
        template_vars['form'] = handle_form(request, directory)
        template_vars['title'] = directory_to_title(directory)
    if request.GET.get('all', False):
        template_vars['notices'] = Notice.objects.filter(directory__pootle_path__startswith=directory.pootle_path).select_related('directory')[:30]
    else:
        template_vars['notices'] = Notice.objects.filter(directory=directory).select_related('directory')[:30]

    if not directory.is_language() and not directory.is_project():
        try:
            request.translation_project = directory.get_translationproject()
            template_vars['navitems'] = [navbar_dict.make_directory_navbar_dict(request, directory)]
            template_vars['translation_project'] = request.translation_project
            template_vars['language'] = request.translation_project.language
            template_vars['project'] = request.translation_project.project
        except:
            pass

    return render_to_response('notices.html', template_vars, context_instance=RequestContext(request))

def directory_to_title(directory):
    """figures out if directory refers to a Language or
    TranslationProject and returns appropriate string for use in
    titles"""

    if directory.is_language():
        trans_vars = {
            'language': tr_lang(directory.language.fullname),
            }
        return _('News for %(language)s', trans_vars)
    elif directory.is_project():
        return _('News for %(project)s', {'project': directory.project.fullname})
    elif directory.is_translationproject():
        trans_vars = {
            'language': tr_lang(directory.translationproject.language.fullname),
            'project': directory.translationproject.project.fullname,
            }
        return _('News for the %(project)s project in %(language)s', trans_vars)
    return _('News for %(path)s',
             {'path': directory.pootle_path})

def handle_form(request, current_directory):
    if request.method == 'POST':
        form = NoticeForm(request.POST)

	#basic validation
        if form.is_valid():
	    #Lets save this NoticeForm, if it is requsted we do that - ie 'publish_rss' is true.
	    if form.cleaned_data['publish_rss'] == True:

		##XXX do we need to do something re: project and language settings

		new_notice = Notice()
		new_notice.message = form.cleaned_data['message']
		new_notice.directory = form.cleaned_data['directory']
	        new_notice.save()

	    #If we want to email it , then do that...
	    if form.cleaned_data['send_email'] == True:
		#print >>sys.stderr , 'Form email is %s' % form.cleaned_data

		email_header = form.cleaned_data['email_header']


		proj_filter = Q()
		lang_filter = Q()
		#Find users to send email too, based on project
		if form.cleaned_data['project_all'] == True:
			projs = Project.objects.all()
		else:
			projs = form.cleaned_data['project_selection']
		#construct the project OR filter
		for proj in projs:
			proj_filter|=Q(projects__exact=proj)

		#Find users to send email too, based on language
		if form.cleaned_data['language_all'] == True:
			langs = Language.objects.all()
		else:
			langs = form.cleaned_data['language_selection']
		#construct the language OR filter
		for lang in langs:
			lang_filter|=Q(languages__exact=lang)
		
		#print >>sys.stderr , 'Project and lang filters are %s\n%s' % (proj_filter, lang_filter)
		#list of pootleprofile objects, linked to User.	

		#XXX Take it account 'only active users' flag from from

		#grab all appropriate Profiles..
		to_list = PootleProfile.objects.filter(lang_filter,proj_filter).distinct()

		#print >>sys.stderr, 'directory is %s' % form.cleaned_data['directory']
		#print >>sys.stderr , 'profile list is %s' % to_list

		to_list_emails = []
		for person in to_list:
			#Check if the User object here as permissions
			if not check_profile_permission(person, 'view', form.cleaned_data['directory']):
				continue
			if person.user.email != '':
				to_list_emails.append(person.user.email)	

		#print >>sys.stderr , 'To list emails is %s' % to_list_emails

		#rest of email settings 
		from_email = DEFAULT_FROM_EMAIL
		message = form.cleaned_data['message']

		#do it.	
		send_mail(email_header, message, from_email, to_list_emails, fail_silently=True)	

	    #return a blank Form to allow user to continue publishing notices
	    # with our defaults
            form = NoticeForm(initial = { 'publish_rss': True , 'directory' : current_directory.pk})
    else:
        form = NoticeForm(initial = { 'publish_rss': True , 'directory' : current_directory.pk} )

    return form


def view_notice_item(request, path, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    template_vars = {
            "title": _("View News Item"),
            "notice_message": notice.message,
            }

    return render_to_response('viewnotice.html', template_vars,
                              context_instance=RequestContext(request))
