# -*- coding: utf-8 -*-
# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

_log = logging.getLogger(__name__)

from datetime import datetime
import time

from werkzeug.exceptions import Forbidden
from werkzeug.utils import secure_filename

from mediagoblin import messages
from mediagoblin import mg_globals

from mediagoblin.auth import lib as auth_lib
from mediagoblin.edit import forms
from mediagoblin.plugins.dogma import forms as dogma_forms
from mediagoblin.plugins.dogma_lib.lib import (list_as_string, save_member_specific_role, get_albums, may_edit_object,
        convert_to_list_of_dicts, save_member_if_new, store_keywords)
from mediagoblin.decorators import (require_active_login, active_user_from_url,
     get_media_entry_by_id,
     user_may_alter_collection, get_user_collection)
from mediagoblin.tools.response import render_to_response, \
    redirect, redirect_obj
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools.text import (
    convert_to_tag_list_of_dicts, media_tags_as_string)
from mediagoblin.tools.url import slugify
from mediagoblin.db.util import check_media_slug_used, check_collection_slug_used
from mediagoblin.plugins.dogma.models import (DogmaBandDB, BandMemberRelationship) 

import mimetypes

@require_active_login
def editMember(request):

    #GET MEMBER
    band = DogmaBandDB.query.filter_by(
        id = request.matchdict['band_id']).first()
    member = BandMemberRelationship.query.filter_by(
        member_id = request.matchdict['member_id'], band_id = band.id).first()
    member_global = member.member_global
    if not may_edit_object(request, member_global, 'creator'):
        raise Forbidden("User may not edit this member")

    defaults = dict(
        member_username_0=member_global.username,
        member_real_name_0=member_global.real_name,
        member_description_0=member_global.description,
        member_since_0 = member.since,
        member_until_0 = member.until,
        )

    #The creation date of the date is turned into milliseconds so it can be used by template's calendar
    band.millis = int(time.mktime(band.since.timetuple())*1000)


    form = dogma_forms.MemberForm(request.form, **defaults)
    #Add the millisecond attribute to the input so it can be used by the JS
    #it needs to be int to be in millis then  turned into str for the WTForm widget
    form.member_since_0.millis = str(int(time.mktime(member.since.timetuple())*1000))
    if member.until:
        form.member_until_0.millis = str(int(time.mktime(member.until.timetuple())*1000))

    return render_to_response(
        request,
        'dogma/edit/edit_member.html',
        {
            'form' : form,
            'member_global' : member_global,
            'member' : member,
            'band' : band
         })

@get_media_entry_by_id
@require_active_login
def editTrack(request, media):
    if not may_edit_object(request, media, 'uploader'):
        raise Forbidden("User may not edit this media")

    defaults = dict(
        title_0=media.title,
        description_0=media.description,
        tags_0=media_tags_as_string(media.tags),
        license_0=media.license,
        )
    form = dogma_forms.DogmaTracks(
        request.form,
        **defaults)
    keywords = media.get_keywords
    if request.method == 'POST' and form.validate():
        #the anti-member-duplicates dict
        existing_members ={}

        #save new roles for each band that has this track (as a collaborator)
        bands = list()
        band_no = 0

        #get all possible bands for all possible albums
        for album in get_albums(media):
            bands.append(album.get_band_relationship[band_no].band)
            band_no += 1

        #store the roles for each bands
        for band in bands:
            #Check if authors or composers field has been changed and process the data if so
            specific_roles = set(["authors", "composers"])
            for role in specific_roles:
                if request.form.get(role+'_0'):
                        existing_members = save_member_specific_role(role, media, band,
                                existing_members, request.form, 0)

            #extra members
            p_key = 0
            pattern = 'No'+str(p_key)+'_0'
            while request.form.get('performer'+pattern):

                #Use this function to get a name and a slug (can be used with a comma separated list)
                dics_list = convert_to_list_of_dicts(request.form.get('performer'+pattern), "username")

                for member_dict in dics_list:
                    #passe the new member alongside to a list of already created users to avoid duplicates
                    existing_members = save_member_if_new(member_dict, existing_members, band)
                    #get this id out of existing members  with the member's slug as a key
                    member_id = existing_members[member_dict["slug"]]
                    #store keywords
                    store_keywords(request.form.get("performer_roles"+pattern), band.id, 
                            member_id, False, media.id, 'role')
                p_key+=1
                pattern = 'No'+str(p_key)+'_0'

        #Delete what you have to among composers/authors or roles
        for author in media.get_authors:
            if int(request.form.get('rm_author_'+str(author.id)) or 0) == author.id:
                author.delete()
        for composer  in media.get_composers:
            if int(request.form.get('rm_composer_'+str(composer.id)) or 0) == composer.id:
                composer.delete()
        for keyword  in media.get_keywords:
            if int(request.form.get('rm_role_'+str(keyword.id)) or 0) == keyword.id:
                keyword.delete()

        if form.title_0.data:
            media.title = form.title_0.data
            media.slug = slugify(media.title)
        media.description = form.description_0.data
        media.tags = convert_to_tag_list_of_dicts(
                               form.tags_0.data)

        media.license = unicode(form.license_0.data) or None
        media.save()

        return redirect_obj(request, media)

    if request.user.is_admin \
            and media.uploader != request.user.id \
            and request.method != 'POST':
        messages.add_message(
            request, messages.WARNING,
            _("You are editing another user's media. Proceed with caution."))

    return render_to_response(
        request,
        'dogma/edit/edit_track.html',
        {'media': media,
         'tracks_form': form,
         'keywords': keywords
         })
