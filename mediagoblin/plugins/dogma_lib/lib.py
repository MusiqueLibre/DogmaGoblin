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
from PIL import Image
from StringIO import StringIO

_log = logging.getLogger(__name__)
from mediagoblin import messages
from mediagoblin.tools.response import redirect
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools import url
from mediagoblin.user_pages.lib import add_media_to_collection
from mediagoblin.db.models import (Collection, CollectionItem)
from mediagoblin.plugins.dogma.models import (DogmaBandDB, DogmaAlbumDB, BandAlbumRelationship, BandMemberRelationship, DogmaMemberDB,
        DogmaKeywordDataDB, DogmaComposerDB, DogmaAuthorDB)

from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker())

class NotSquare(Exception):
    pass

def save_pic(request,input_name, path, element_id, album_cover = False): 
    if request.files[input_name]:
        #Adding band picture
        band_pic = Image.open(StringIO(request.files[input_name].read()))

        #If it's an album cover it must be a square
        print band_pic.size[0],band_pic.size[1]
        if not band_pic.size[0] == band_pic.size[1]:
            print 'bou'
        #save the original image
        band_pic.save(path+'/'+str(element_id)+".jpeg", "JPEG")
        #create the thumbnail...
        band_pic.thumbnail((400,400), Image.ANTIALIAS)
        #...and save it
        band_pic.save(path+"/thumbs/"+str(element_id)+"_th.jpeg", "JPEG")

def album_lib(request, form, redirect_path, band,  is_album = False):
    # If we are here, method=POST and the form is valid, submit things.
    # If the user is adding a new collection, use that:
    if form.collection_title.data:

        collection = Collection()
        collection.title = unicode(form.collection_title.data)
        collection.description = unicode(form.collection_description.data)
        collection.creator = request.user.id
        collection.generate_slug()

        # Make sure this user isn't duplicating an existing collection
        existing_albums = band.albums
        albums_names = list()
        for album in existing_albums:
            albums_names.append(album.album.get_collection.title)

        if collection.title in albums_names:
            messages.add_message(request, messages.ERROR,
                _('You already have a album called "%s"!')
                % collection.title)
            return
        else:
            collection.save()


        #save it to the album table if it is one
        if is_album:
            album = request.db.DogmaAlbumDB()
            album.id = collection.id
            album.release_date = form.release_date.data
            album.save()
            #check if the relation exists
            #STORE THE BAND/ALBUM RELATIONSHIP
            band_relation = request.db.BandAlbumRelationship()
            existing_relation = BandAlbumRelationship.query.filter_by(
                                    album_id=band_relation.album_id,
                                    band_id=band_relation.band_id).first()
            #if it doesn't create it
            if not existing_relation :
                band_relation.band_id = request.form.get('band')
                band_relation.album_id = collection.id
                band_relation.save()

    # Otherwise, use the collection selected from the drop-down
    else:
        collection = form.collection.data
        if collection and collection.creator != request.user.id:
            collection = None


    return collection

def add_to_album( request, media, collection, redirect_path):

    # Make sure the user actually selected a collection
    if not collection:
        empty_error_msg = 'You have to select or add a collection'
        if is_album:
            empty_error_msg = 'You have to select or create an album'
        messages.add_message(
            request, messages.ERROR,
            _(empty_error_msg))
        return redirect(request, redirect_path,
                    user=media.get_uploader.username,
                    media_id=media.id)
    # Check whether media already exists in collection
    if CollectionItem.query.filter_by(
        media_entry=media.id,
        collection=collection.id).first():
        messages.add_message(request, messages.ERROR,
                             _('"%s" already in collection "%s"')
                             % (media.title, collection.title))
    else: # Add item to collection
        add_media_to_collection(collection, media)

        messages.add_message(request, messages.SUCCESS,
                             
                _('"%s" added to collection "%s"')
                             % (media.title, collection.title))



def convert_to_list_of_dicts(multiple_string, _type):
    """
    Filter input from incoming string containing user words/names etc...,

    this is the generic version of the regular tag tools found in tools/text.py
    """
    wordlist = []
    if multiple_string:

        # Strip out internal, trailing, and leading whitespace
        stripped_multiple_string = u' '.join(multiple_string.strip().split())

        # Split the string into a list of words
        for word in stripped_multiple_string.split(','):
            word = word.strip()
            # Ignore empty or duplicates
            if word and word not in [t[_type] for t in wordlist]:
                wordlist.append({_type: word,
                                'slug': url.slugify(word)})
    return wordlist

def save_member_if_new(member_dict, existing_members, band):
     #check if the member exists
     if not member_dict["slug"] in existing_members:
         member = DogmaMemberDB()
         member.username = member_dict["username"]
         member.slug = member_dict["slug"]
         member.save()

         member_band_relationship = BandMemberRelationship()
         member_band_relationship.band_id = band.id
         member_band_relationship.member_id = member.id
         member_band_relationship.main = False
         member_band_relationship.save()

         #add this member to the existing members to prevent duplicates
         existing_members[member_dict["slug"]] =  member.id
         member_id = member.id

     return existing_members


def save_member_specific_role(current_role, entry, band, existing_members, request_form, key):

    #Get the general input if empty, else take the track list
    new_members_list = request_form.get(current_role+"_"+str(key)) if request_form.get(current_role+"_"+str(key)) \
        else request_form.get(current_role)
    #create a dictionnary out of the new members' list
    dics_list = convert_to_list_of_dicts(new_members_list, "username")
    for member_dict in dics_list :
        #passe the new member alongside to a list of already created users to avoid duplicates
        existing_members = save_member_if_new(member_dict, existing_members, band)

        #get this id out of existing members  with the member's slug as a key
        member_id = existing_members[member_dict["slug"]]

        _log.info(existing_members)

        if current_role == "authors":
            table = DogmaAuthorDB()
        elif current_role == "composers":
            table = DogmaComposerDB()
        table.media_entry = entry.id
        table.member = member_id
        table.save()

    return existing_members

def store_keywords(keywords_input, band, member, album,  media_entry, _type):
    # store roles as keywords using the tags tools
    keyword_list = convert_to_list_of_dicts(keywords_input, "username")
    for  my_keyword in keyword_list:
        keywords = DogmaKeywordDataDB()
        keywords.data = my_keyword['username']
        keywords.slug = my_keyword['slug']

        #The keywords can be linked to any albums/band/members/tracks
        if band :
            keywords.band = band
        if album :
            keywords.album = album
        if member :
            keywords.member= member
        if media_entry:
            keywords.media_entry = media_entry
        keywords.type = _type
        keywords.save()

def list_as_string(_list, attribute, params):
    """
    This is a generic function to turn any forms of keywords/authors/comma-separated-mutlti-values
    into the string it's been generated from. You need two arguments : the backref to get the proper
    table, then the attribute with the original name/keyword

    """
    list_string = ''
    if _list:
        #Check the params : if the params value and the object value don't matche, you don't want the keyword
        for list_entry in _list:
            for k, v in params.items():
                if not getattr(list_entry,k) == v:
                    _list.remove(list_entry)
        list_string = u', '.join([getattr(entry, attribute) for entry in _list])
    return list_string

def complete_band_list():
  bands = DogmaBandDB.query.all()
  bands_list = list()
  for band in bands:
      bands_list.append(band.name)
  return bands_list

#get the albums of a media
def get_albums(media):
    albums = list()
    for collection in media.collections:
        albums.append(collection.get_album)
    return albums


def may_edit_object(request, _object, check_this_id):
    """Check, if the request's user may edit the media details"""
    if getattr(_object, check_this_id) == request.user.id:
        return True
    if request.user.is_admin:
        return True
    return False

def check_if_ajax(request):
    if 'ajax' in request.GET:
        return True
    return False
