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
from mediagoblin import messages
from mediagoblin.db.models import Collection

from mediagoblin.plugins.dogma_extra_data.models import DogmaAlbumDB,BandAlbumRelationship

def collection_tools(request, media, form, redirect_path, is_album = False):
    _log.info(media)
    _log.info('THIS IS HERE')
    # If we are here, method=POST and the form is valid, submit things.
    # If the user is adding a new collection, use that:
    if form.collection_title.data:
        # Make sure this user isn't duplicating an existing collection
        existing_collection = Collection.query.filter_by(
                                creator=request.user.id,
                                title=form.collection_title.data).first()
        if existing_collection:
            messages.add_message(request, messages.ERROR,
                _('You already have a collection called "%s"!')
                % existing_collection.title)
            return redirect(request, redirect_path,
                            user=media.get_uploader.username,
                            media=media.slug_or_id)

        collection = Collection()
        collection.title = form.collection_title.data
        collection.description = form.collection_description.data
        collection.creator = request.user.id
        collection.generate_slug()
        collection.save()




    # Otherwise, use the collection selected from the drop-down
    else:
        collection = form.collection.data
        if collection and collection.creator != request.user.id:
            collection = None



    # Make sure the user actually selected a collection
    if not collection:
        empty_error_msg = 'You have to select or add a collection'
        if is_album:
            empty_error_msg = 'You have to select or create an album'
        messages.add_message(
            request, messages.ERROR,
            _(empty_error_msg))
        return redirect(redirect__path)
    # Check whether media already exists in collection
    if CollectionItem.query.filter_by(
        media_entry=media.id,
        collection=collection.id).first():
        messages.add_message(request, messages.ERROR,
                             _('"%s" already in collection "%s"')
                             % (media.title, collection.title))
    else: # Add item to collection
        collection_item = request.db.CollectionItem()
        collection_item.collection = collection.id
        collection_item.media_entry = media.id
        collection_item.note = form.note.data
        collection_item.save()

        collection.items = collection.items + 1
        collection.save()

        media.collected = media.collected + 1
        media.save()

        messages.add_message(request, messages.SUCCESS,
                             _('"%s" added to collection "%s"')
                             % (media.title, collection.title))

    #save it to the album table if it is one
    if is_album:
        album = request.DogmaAlbumDB
        album.id = collection.id
        album.save()
        return collection.id
