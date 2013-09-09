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
from mediagoblin import messages
import mediagoblin.mg_globals as mg_globals
from os.path import splitext

import os
import logging

_log = logging.getLogger(__name__)

from werkzeug.datastructures import FileStorage
from StringIO import StringIO
import pprint
from datetime import datetime
import time

from pprint import pprint

from mediagoblin.tools import url
from mediagoblin.tools.text import convert_to_tag_list_of_dicts
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools.response import render_to_response, redirect, render_404
from mediagoblin.tools.pagination import Pagination
from mediagoblin.decorators import (require_active_login,active_user_from_url, uses_pagination, user_may_delete_media, 
        get_media_entry_by_id, user_may_alter_collection, get_user_collection, get_user_collection_item)
#from mediagoblin.submit import forms as submit_forms
from mediagoblin.messages import add_message, SUCCESS, ERROR
from mediagoblin.media_types import sniff_media, \
    InvalidFileType, FileTypeNotSupported
from mediagoblin.submit.lib import run_process_media, prepare_queue_task

#ADDING ALBUM TOOLS
from mediagoblin.plugins.dogma_lib.lib import (album_lib, add_to_album, save_pic, get_albums,
        convert_to_list_of_dicts, save_member_specific_role, save_member_if_new, store_keywords)
from mediagoblin.db.models import (MediaEntry, Collection,  User, MediaFile)
from mediagoblin.user_pages import forms as user_forms

#BAND
from mediagoblin.plugins.dogma import forms as dogma_form
from mediagoblin.plugins.dogma.models import (DogmaBandDB, DogmaMemberDB,  BandMemberRelationship, DogmaAlbumDB, BandAlbumRelationship,
                                              BandAlbumRelationship, DogmaAuthorDB, DogmaComposerDB)

@require_active_login
def addBand(request):
    band_form = dogma_form.BandForm(request.form)

    #Process band data
    if request.method == 'POST' and band_form.validate():

        #create a new band
        band = DogmaBandDB()

        band.name = unicode(request.form.get('band_name'))
        band.description = unicode(request.form.get('band_description'))
        #geoloc details
        for item in ['place', 'country', 'latitude', 'longitude']:
            #It returns an error if an empty string is given, I have to replace it with "None" for it to work properly
            if request.form.get(item+"_0") == '':
                data = None 
            else:
                data = unicode(request.form.get(item+"_0"))
            setattr(band, item, data)
        #user data
        print "bou"
        band.creator = unicode(request.user.id)
        band.since =  request.form.get('band_since')
        band.subscribed_since = datetime.now().strftime("%Y-%m-%d")

        band.save()

        save_pic(request,'band_picture',os.path.abspath("mediagoblin/plugins/dogma/static/images/uploaded/band_photos"), band.id)


        if "submit_and_continue" in request.form:
            return redirect(request, "mediagoblin.plugins.dogma.add_members",
                                current_band=band.id)
        else:
            return redirect(request, "mediagoblin.plugins.dogma.dashboard",
                                user=request.user.username,
                           )

    return render_to_response(
            request,
            'dogma/add_band.html',
            {
              'band_form': band_form,
            }
            )

@require_active_login
def addMembers(request):
    band = DogmaBandDB.query.filter_by(
        id = request.GET['current_band']).first()
    #check for user's right
    if band.creator != request.user.id:
        return render_to_response(
                request,
                'dogma/errors/not_allowed.html',
                {
                  'band': band,
                  'user': request.user
                }
                )

    member_form = dogma_form.MemberForm(request.form)

    #The creation date of the date is turned into milliseconds so it can be used by template's calendar
    band.millis = int(time.mktime(band.since.timetuple())*1000)

    if request.method == 'POST' and member_form.validate():
        #Members
        member_index = 0
        #loop the members and save them all
        while request.form.get('member_since_'+str(member_index)):
            member = DogmaMemberDB()
            member.username =  request.form.get('member_username_'+str(member_index))
            member.slug = url.slugify(member.username)
            member.real_name =  request.form.get('member_real_name_'+str(member_index))
            member.description =  request.form.get('member_description_'+str(member_index))
            member.place =  request.form.get('place_'+str(member_index))
            member.country =  request.form.get('country_'+str(member_index))
            member.latitude =  request.form.get('latitude_'+str(member_index))
            member.longitude =  request.form.get('longitude_'+str(member_index))
            member.creator = request.user.id
            member.save()

            #store this member's data for the current band using many to many relationship
            member_band_data = BandMemberRelationship()
            member_band_data.band_id =  band.id
            member_band_data.member_id = member.id
            member_band_data.since =   request.form.get('member_since_'+str(member_index))
            member_band_data.roles =   request.form.get('member_roles_'+str(member_index))
            #The member is supposedly active. People might make a member a "former member"
            if request.form.get('member_former_'+str(member_index)):
                member_band_data.former = True
                member_band_data.until =   request.form.get('member_until_'+str(member_index))
            else:
                member_band_data.former = False
            member_band_data.main =  form.member_main.data
            member_band_data.save()

            save_pic(request,'member_picture_'+str(member_index),os.path.abspath("mediagoblin/plugins/dogma/static/images/uploaded/member_photos"), member.id)

            #Next member to save 
            member_index += 1

        if "submit_and_continue" in request.form:
            return redirect(request, "mediagoblin.plugins.dogma.add_album",
                                current_band=band.id)
        else:
            return redirect(request, "mediagoblin.plugins.dogma.dashboard",
                                user=request.user.username,
                           )

    return render_to_response(
            request,
            'dogma/add_members.html',
            {
              'member_form': member_form,
              'band': band
            }
            )

@require_active_login
def addAlbum(request):
    #BANDS
    band = DogmaBandDB.query.filter_by(
        id = request.GET['current_band'], creator = request.user.id).first()

    #The creation date of the date is turned into milliseconds so it can be used by template's calendar
    key = 0
    for member in band.members:
        band.members[key].millis_since = int(time.mktime(member.since.timetuple())*1000)
        if member.until:
            band.members[key].millis_until = int(time.mktime(member.until.timetuple())*1000)
        else:
            band.members[key].millis_until = False
        key += 1

    #ALBUMS/COLLECTIONS
    collection_form = dogma_form.AlbumForm(request.form)


    if request.method == 'POST' and collection_form.validate():

        #STORE THE ALBUM
        collection = album_lib(request, collection_form, \
                    'mediagoblin.plugins.dogma.add_tracks',band, True)
        if not collection:
            return redirect(request, 'mediagoblin.plugins.dogma.add_album', current_band=band.id)


        save_pic(request,'album_picture',\
                os.path.abspath("mediagoblin/plugins/dogma/static/images/uploaded/album_covers"), collection.id, True)

        #ROLES
        role_index = 0
        #loop the members and save them all
        while not request.form.get('roles_'+str(role_index)) == None:
            # store roles as keywords using the tags tools
            store_keywords(request.form.get("roles_"+str(role_index)), False, 
                    request.form.get("member_"+str(role_index)), collection.id, False, 'role')
            role_index += 1

        if "submit_and_continue" in request.form:
            return redirect(request, "mediagoblin.plugins.dogma.add_tracks",
                                current_band=band.id,
                                current_album=collection.id)
        else:
            return redirect(request, "mediagoblin.plugins.dogma.dashboard",
                                     user=request.user.username,
                               )
    return render_to_response(
            request,
            'dogma/add_album.html',
            {
             'collection_form': collection_form,
             'band': band,
            }
            )
@require_active_login
def addTracks(request):
    #BANDS
    band = DogmaBandDB.query.filter_by(
        id = request.GET['current_band'], creator = request.user.id).first()
    #ALBUM
    album = Collection.query.filter_by(
        id = request.GET['current_album'], creator = request.user.id).first()
    #TRACKS
    #Global
    tracks_form_global = dogma_form.DogmaTracksGlobal(request.form,
        license=request.user.license_preference)
    #Per track
    tracks_form = dogma_form.DogmaTracks(request.form,
        license=request.user.license_preference)

    if request.method == 'POST':
        #Use this to check for valid files
        found_valid_file = False
        existing_members ={} 
        key = 0
        for submitted_file in request.files.getlist('file[]'):
            try:
                if not submitted_file.filename:
                    # MOST likely an invalid file
                    continue # Skip the rest of the loop for this file
                else:
                    found_valid_file = True # We found a file!

                filename = submitted_file.filename


                # Sniff the submitted media to determine which
                # media plugin should handle processing
                media_type, media_manager = sniff_media(
                    submitted_file)
                if not media_type == 'mediagoblin.media_types.audio':
                    add_message(request, ERROR, _('You can only upload audiofiles here. '+submitted_file.filename+' have been skipped'))
                    continue
                # create entry and save in database
                entry = request.db.MediaEntry()
                entry.media_type = unicode(media_type)
                entry.title = (
                    unicode(request.form.get('title_'+str(key)))
                    or unicode(splitext(filename)[0]))

                entry.description = unicode(request.form.get('description_'+str(key)))

                #Use the global license if there's no specific license for this track
                if request.form.get('license_'+str(key)) == '__none':
                    entry.license = unicode(request.form.get('license'))
                else:
                    entry.license = unicode(request.form.get('license_'+str(key)))

                entry.uploader = request.user.id

                #Append track's tags to global ones
                tags_global = request.form.get('tags')
                tags_track = request.form.get('tags_'+str(key))

                #Transform "none" into an empty string to prevent errors 
                tags_global = '' if tags_track == None else tags_global
                tags_track = '' if tags_track == None else tags_track
                
                tags = tags_global+','+tags_track
                # Process the user's folksonomy "tags"
                entry.tags = convert_to_tag_list_of_dicts(tags)

                # Generate a slug from the title
                entry.generate_slug()

                queue_file = prepare_queue_task(request.app, entry, filename)

                with queue_file:
                    queue_file.write(submitted_file.stream.read())

                # Save now so we have this data before kicking off processing
                entry.save()

                #Composers and Authors
                # python2.7 syntaxe :specific_roles = {"authors", "composers"}
                specific_roles = set(["authors", "composers"])
                for role in specific_roles:
                    existing_members = save_member_specific_role(role, entry, band,
                            existing_members, request.form, key)

                #extra members
                p_key = 0
                pattern = 'No'+str(p_key)+'_'+str(key)
                while request.form.get('performer'+pattern):

                    #Use this function to get a name and a slug (can be used with a comma separated list)
                    dics_list = convert_to_list_of_dicts(request.form.get('performer'+pattern), "username")
                    _log.info(convert_to_list_of_dicts)

                    for member_dict in dics_list:
                        #passe the new member alongside to a list of already created users to avoid duplicates
                        existing_members = save_member_if_new(member_dict, existing_members, band)
                        #get this id out of existing members  with the member's slug as a key
                        member_id = existing_members[member_dict["slug"]]
                        #store keywords
                        store_keywords(request.form.get("performer_roles"+pattern), band.id, 
                                member_id, album.id, entry.id, 'role')
                    p_key+=1
                    pattern = 'No'+str(p_key)+'_'+str(key)





                #add the media to collection/album
                add_to_album(request, entry, album, \
                                  'mediagoblin.plugins.dogma.add_tracks')
                # Pass off to processing
                #
                # (... don't change submitted file after this point to avoid race
                # conditions with changes to the document via processing code)
                feed_url = request.urlgen(
                    'mediagoblin.user_pages.atom_feed',
                    qualified=True, user=request.user.username)
                run_process_media(entry, feed_url)
                add_message(request, SUCCESS, _('Woohoo! Submitted!'))

            except Exception as e:
                '''
                This section is intended to catch exceptions raised in
                mediagoblin.media_types
                '''
                error_tuple = tracks_form_global.tracks.errors
                if isinstance(e, InvalidFileType) or \
                        isinstance(e, FileTypeNotSupported):
                    messages.add_message(request, messages.ERROR,
                                 _(u'A file has been skipped. Only audiofiles are supported'))
                else:
                    raise
            key += 1
        if not found_valid_file:
            messages.add_message(request, messages.ERROR,
                                 _(u'You must provide a file.'))
        else:
            return redirect(request, "mediagoblin.user_pages.user_home",
                            user=request.user.username)
    return render_to_response(
            request,
            'dogma/add_tracks.html',
            {
             'tracks_form_global': tracks_form_global,
             'tracks_form': tracks_form,
             'band': band,
             'album': album,
            }
            )



@require_active_login
def dashboard(request):
    #BANDS
    bands = DogmaBandDB.query.filter_by(
        creator = request.user.id)
    return render_to_response(
            request,
            'dogma/dashboard.html',
            {
                'bands': bands,
            }
            )
@uses_pagination
def albumPage(request, page):
    """A User-defined Collection"""
    collection = Collection.query.filter_by(
        slug=request.matchdict['collection']).first()

    if not collection:
        return render_404(request)

    collection_items = collection.get_collection_items()

    item_list = list()
    #create the list for the filter
    for item in collection_items:
        item_list.append(item.media_entry)

    # A query for the path
    media_files = MediaFile.query.filter_by(name_id = 3)\
        .filter(MediaFile.media_entry.in_(item_list)).order_by(MediaFile.media_entry)
    # A query for the name
    media_entry = MediaEntry.query\
            .filter(MediaEntry.id.in_(item_list)).order_by(MediaEntry.id)


    medias = list()

    i=0
    for my_file in media_files:
        media = {'path': "/".join(my_file.file_path), 'title': media_entry[i].title}
        medias.append(media)
        i+=1

    # if no data is available, return NotFound
    # TODO: Should an empty collection really also return 404?
    if collection_items == None:
        return render_404(request)

    return render_to_response(
        request,
        'dogma/album.html',
        {
         'collection': collection,
         'collection_items': collection_items,
         'medias': medias
         })
#CORE CONTROLERS OVERRIDE
def rootViewDogma(request):

    bands = DogmaBandDB.query
    band_selected = False # is checked in the template and have to be set
    band_selected_id = False # is checked in the template and have to be set
    if 'current_band' in request.GET:
        band_selected_id = int(request.GET['current_band']) 
        band_selected = DogmaBandDB.query.filter_by(
            id = band_selected_id ).first()
    return render_to_response(
        request, 'mediagoblin/root.html',
        {
            'bands' : bands,
            'band_selected': band_selected,
            'band_selected_id': band_selected_id,
         })


@get_user_collection
@require_active_login
@user_may_alter_collection
def album_confirm_delete(request, collection):

    form = user_forms.ConfirmDeleteForm(request.form)

    if request.method == 'POST' and form.validate():

        username = collection.get_creator.username

        if form.confirm.data is True:
            collection_title = collection.title

            # Delete all the associated collection items and tracks
            for item in collection.get_collection_items():
                entry = item.get_media_entry
                entry.collected = entry.collected - 1
                entry.save()
                item.delete()

            # Delete the album
            for relation in BandAlbumRelationship.query.filter_by(album_id = collection.id):
                relation.delete()
            DogmaAlbumDB.query.filter_by(id = collection.id).delete()


            collection.delete()
            messages.add_message(request, messages.SUCCESS,
                _('You deleted the collection "%s"') % collection_title)

            return redirect(request, "mediagoblin.plugins.dogma.dashboard",
                user=username)
        else:
            messages.add_message(
                request, messages.ERROR,
                _("The collection was not deleted because you didn't check that you were sure."))

            return redirect_obj(request, collection)

    if ((request.user.is_admin and
         request.user.id != collection.creator)):
        messages.add_message(
            request, messages.WARNING,
            _("You are about to delete another user's collection. "
              "Proceed with caution."))

    return render_to_response(
        request,
        'mediagoblin/user_pages/collection_confirm_delete.html',
        {'collection': collection,
         'form': form})


