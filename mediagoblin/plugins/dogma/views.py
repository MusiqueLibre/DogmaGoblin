
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

import logging

_log = logging.getLogger(__name__)

from werkzeug.datastructures import FileStorage
import Image
from StringIO import StringIO
import pprint
from datetime import datetime
import time

from pprint import pprint

from mediagoblin.tools.text import convert_to_tag_list_of_dicts
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools.response import render_to_response, redirect
from mediagoblin.tools.pagination import Pagination
from mediagoblin.decorators import require_active_login,active_user_from_url, uses_pagination
#from mediagoblin.submit import forms as submit_forms
from mediagoblin.messages import add_message, SUCCESS
from mediagoblin.media_types import sniff_media, \
    InvalidFileType, FileTypeNotSupported
from mediagoblin.submit.lib import run_process_media, prepare_queue_task

#ADDING ALBUM TOOLS
from mediagoblin.plugins.dogma_tools.album import collection_tools, add_to_collection
from mediagoblin.db.models import (MediaEntry, Collection,  User, MediaFile)
from mediagoblin.user_pages import forms as user_forms

#BAND
from mediagoblin.plugins.dogma import forms as dogma_form
from mediagoblin.plugins.dogma.models import (DogmaBandDB, DogmaMemberDB, 
                                                         BandMemberRelationship, BandAlbumRelationship)



@require_active_login
def addAlbum(request):
    #BANDS
    band = DogmaBandDB.query.filter_by(
        id = request.GET['current_band'], creator = request.user.id).first()
    #ALBUMS/COLLECTIONS
    collection_form = dogma_form.AlbumForm(request.form)


    #check is collection/album is empty
    if request.method == 'POST' and collection_form.validate():
        #STORE THE ALBUM
        collection = collection_tools(request, collection_form, \
                    'mediagoblin.plugins.dogma.add_tracks', True)


        savePic(request,'album_cover',"mediagoblin/plugins/dogma/uploaded_images/album_covers/", collection.id)

        if "submit_and_continue" in request.form:
            return redirect(request, "mediagoblin.plugins.dogma.add_tracks",
                                current_band=band.id)
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
    #TRACKS
    submit_form_global = dogma_form.DogmaSubmitFormGlobal(request.form,
        license=request.user.license_preference)
    submit_form_track = dogma_form.DogmaSubmitFormTrack(request.form,
        license=request.user.license_preference)

    if request.method == 'POST' and submit_form_track.validate():
        #index of the for loop (must but a better way)
        i = 0
        for submitted_file in request.files.iteritems(multi=True):
            #if not ('file' in submitted_file
                    #and isinstance(submitted_file[1], FileStorage)
                    #and submitted_file[1].stream):
                #messages.add_message(request, messages.ERROR,
                                     #_(u'You must provide a file.'))
            #else:
                try:
                    current_file = request.files.getlist('file[]')[i]
                    filename = current_file.filename

                    # Sniff the submitted media to determine which
                    # media plugin should handle processing
                    media_type, media_manager = sniff_media(
                        current_file)

                    # create entry and save in database
                    entry = request.db.MediaEntry()
                    entry.media_type = unicode(media_type)
                    entry.title = (
                        unicode(request.form.get('title_'+str(i)))
                        or unicode(splitext(filename)[0]))

                    entry.description = unicode(request.form.get('description_'+str(i)))

                    #Use the global license if there's no specific license for this track
                    if not request.form.get('license_'+str(i)) :
                        entry.license = unicode(request.form.get('license'))
                    else:
                        entry.license = unicode(request.form.get('license_'+str(i)))

                    entry.uploader = request.user.id

                    #Append track's tags to global ones
                    tags = request.form.get('tags')+','+request.form.get('tags_'+str(i))
                    # Process the user's folksonomy "tags"
                    entry.tags = convert_to_tag_list_of_dicts(tags)

                    # Generate a slug from the title
                    entry.generate_slug()

                    queue_file = prepare_queue_task(request.app, entry, filename)

                    with queue_file:
                        queue_file.write(current_file.stream.read())

                    # Save now so we have this data before kicking off processing
                    entry.save()

                    #Extra data for dogma
                    entry_extra = request.db.DogmaExtraDataDB()

                    entry_extra.media_entry = entry.id
                    entry_extra.composers = unicode(request.form.get('composers_'+str(i)))
                    entry_extra.authors = unicode(request.form.get('authors_'+str(i)))
                    entry_extra.performers = unicode(request.form.get('performers_'+str(i)))

                    entry_extra.save()

                    #add the media to collection
                    add_to_collection(request, entry, collection_form, collection, \
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

                    #increment index
                    i+= 1

                except Exception as e:
                    '''
                    This section is intended to catch exceptions raised in
                    mediagoblin.media_types
                    '''
                    if isinstance(e, InvalidFileType) or \
                            isinstance(e, FileTypeNotSupported):
                             submitted_file[i].errors.append(
                            e)
                    else:
                        raise
        return redirect(request, "mediagoblin.user_pages.user_home",
                        user=request.user.username)
    return render_to_response(
            request,
            'dogma/add_tracks.html',
            {
             'submit_form_global': submit_form_global,
             'submit_form_track': submit_form_track,
             'band': band,
            }
            )
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
        band.postalcode = unicode(request.form.get('band_postalcode'))
        band.place = unicode(request.form.get('band_place'))
        band.country = unicode(request.form.get('band_country'))
        band.latitude = unicode(request.form.get('band_latitude'))
        band.longitude = unicode(request.form.get('band_longitude'))
        #user data
        band.creator = unicode(request.user.id)
        band.since =  request.form.get('band_since')
        band.subscribed_since = datetime.now().strftime("%Y-%m-%d")

        band.save()

        savePic(request,'band_picture',"mediagoblin/plugins/dogma/uploaded_images/band_photos/", band.id)


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
def addMembers(request):
    member_form = dogma_form.MemberForm(request.form)
    band = DogmaBandDB.query.filter_by(
        id = request.GET['current_band'], creator = request.user.id).first()
    band.millis = int(time.mktime(band.since.timetuple())*1000)
    if request.method == 'POST' and member_form.validate():
        #Members

        member_index = 0
        #loop the members and save them all
        while request.form.get('member_roles_'+str(member_index)):
            member = DogmaMemberDB()
            member.first_name =  request.form.get('member_first_name_'+str(member_index))
            member.last_name =  request.form.get('member_last_name_'+str(member_index))
            member.nickname =  request.form.get('member_nickname_'+str(member_index))
            member.description =  request.form.get('member_description_'+str(member_index))
            member.place =  request.form.get('member_place_'+str(member_index))
            member.country =  request.form.get('member_country_'+str(member_index))
            member.latitude =  request.form.get('member_latitude_'+str(member_index))
            member.longitude =  request.form.get('member_longitude_'+str(member_index))
            member.creator = request.user.id
            member.save()

            #store this member's data for the current band using many to many relationship
            member_band_data = BandMemberRelationship()
            member_band_data.band_id =  band.id
            member_band_data.member_id = member.id
            member_band_data.since =   request.form.get('member_since_'+str(member_index))
            member_band_data.roles =   request.form.get('member_roles_'+str(member_index))
            #The member is supposedly active. People might make a member a "former member"
            member_band_data.former = False
            member_band_data.save()

            savePic(request,'member_picture_'+str(member_index),"mediagoblin/plugins/dogma/uploaded_images/member_photos/", member.id)

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

def savePic(request,input_name, path, element_id): 
    if request.files[input_name]:
        #Adding band picture
        band_pic = Image.open(StringIO(request.files[input_name].read()))
        #save the original image
        band_pic.save(path+str(element_id)+".jpeg", "JPEG")
        #create the thumbnail...
        band_pic.thumbnail((400,400), Image.ANTIALIAS)
        #...and save it
        band_pic.save(path+"thumbs/"+str(element_id)+"_th.jpeg", "JPEG")


@require_active_login
def dashboard(request):
    #BANDS
    bands = DogmaBandDB.query.filter_by(
        creator = request.user.id)
    complete_list = list()
    for my_band in bands:
        complete_list.append({'band': my_band, 'members':getMembers(my_band, request.user.id), 'albums': getAlbums(my_band, request.user.id)})
    return render_to_response(
            request,
            'dogma/dashboard.html',
            {
                'complete_list': complete_list,
            }
            )
@uses_pagination
@active_user_from_url
def user_album(request, page, url_user=None):
    """A User-defined Collection"""
    collection = Collection.query.filter_by(
        get_creator=url_user,
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
        {'user': url_user,
         'collection': collection,
         'collection_items': collection_items,
         'medias': medias
         })

###########################
### Cross-views methods ###
##########################
def getAlbums(band, user_id):
    #get the albums of a band
    band_albums = BandAlbumRelationship.query.filter_by(
        band_id = band.id)
    album_id_list = list()
    #create the list of albums ids for the filter
    for album in band_albums:
        album_id_list.append(album.album_id)

    # return the list of collections that match the album id
    return Collection.query.filter_by(
            creator = user_id, ).order_by(Collection.title).filter(Collection.id.in_(album_id_list))

def getMembers(band, user_id):
    #get the members of a band
    band_members = BandMemberRelationship.query.filter_by(
        band_id = band.id)
    members_id_list = list()
    #create the list for the filter
    for member in band_members:
        members_id_list.append(member.member_id)

    #Get the general data for each member
    members_global_data = DogmaMemberDB.query.filter_by(
                creator = user_id ).filter(DogmaMemberDB.id.in_(members_id_list))

    #Merge the two
    i=0
    members = list()
    for member in band_members:
        members.append({'specific':member, 'global':members_global_data[i]})
        i+=1

    return members
