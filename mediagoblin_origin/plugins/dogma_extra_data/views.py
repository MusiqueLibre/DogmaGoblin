
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

from mediagoblin.tools.text import convert_to_tag_list_of_dicts
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools.response import render_to_response, redirect
from mediagoblin.decorators import require_active_login
from mediagoblin.submit import forms as submit_forms
from mediagoblin.messages import add_message, SUCCESS
from mediagoblin.media_types import sniff_media, \
    InvalidFileType, FileTypeNotSupported
from mediagoblin.submit.lib import run_process_media, prepare_queue_task
#ADDING COLLECTIONS
from mediagoblin.tools.collection import collection_tools
from mediagoblin.db.models import (MediaEntry, Collection, CollectionItem, User)
from mediagoblin.user_pages import forms as user_forms

#BAND
from mediagoblin.plugins.dogma_extra_data import forms as dogma_form



@require_active_login
def process_extra_data(request):
    submit_form = submit_forms.SubmitStartForm(request.form,
        license=request.user.license_preference)
    #ADDING
    collection_form = user_forms.MediaCollectForm(request.form)
    # A user's own collections:
    collection_form.collection.query = Collection.query.filter_by(
        creator = request.user.id).order_by(Collection.title)

    if request.method == 'POST' and submit_form.validate():
        if not ('file' in request.files
                and isinstance(request.files['file'], FileStorage)
                and request.files['file'].stream):
            submit_form.file.errors.append(
                _(u'You must provide a file.'))
        else:
            try:
                filename = request.files['file'].filename

                # Sniff the submitted media to determine which
                # media plugin should handle processing
                media_type, media_manager = sniff_media(
                    request.files['file'])

                # create entry and save in database
                entry = request.db.MediaEntry()
                entry.media_type = unicode(media_type)
                entry.title = (
                    unicode(request.form['title'])
                    or unicode(splitext(filename)[0]))

                entry.description = unicode(request.form.get('description'))

                entry.license = unicode(request.form.get('license', "")) or None

                entry.uploader = request.user.id

                # Process the user's folksonomy "tags"
                entry.tags = convert_to_tag_list_of_dicts(
                    request.form.get('tags'))

                # Generate a slug from the title
                entry.generate_slug()

                queue_file = prepare_queue_task(request.app, entry, filename)

                with queue_file:
                    queue_file.write(request.files['file'].stream.read())

                # Save now so we have this data before kicking off processing
                entry.save()

                #Extra data for dogma
                entry_extra = request.db.DogmaExtraDataDB()

                entry_extra.media_entry = entry.id
                entry_extra.composers = unicode(request.form.get('composers'))
                entry_extra.authors = unicode(request.form.get('authors'))
                entry_extra.performers = unicode(request.form.get('performers'))

                entry_extra.save()

                #Add the media to a collection if you want
                collection_tools(request, entry,collection_form, new_media=True)

                # Pass off to processing
                #
                # (... don't change entry after this point to avoid race
                # conditions with changes to the document via processing code)
                feed_url = request.urlgen(
                    'mediagoblin.user_pages.atom_feed',
                    qualified=True, user=request.user.username)
                run_process_media(entry, feed_url)
                add_message(request, SUCCESS, _('Woohoo! Submitted!'))

                return redirect(request, "mediagoblin.user_pages.user_home",
                                user=request.user.username)
            except Exception as e:
                '''
                This section is intended to catch exceptions raised in
                mediagoblin.media_types
                '''
                if isinstance(e, InvalidFileType) or \
                        isinstance(e, FileTypeNotSupported):
                    submit_form.file.errors.append(
                        e)
                else:
                    raise
    return render_to_response(
            request,
            'dogma_extra_data/dogma_submit.html',
            {
             'submit_form': submit_form,
             'collection_form': collection_form,
            }
            )
@require_active_login
def add_band(request):
    band_form = dogma_form.BandForm(request.form)
    member_form = dogma_form.MemberForm(request.form)
    return render_to_response(
            request,
            'dogma_extra_data/add_band.html',
            {
              'band_form': band_form,
              'member_form': member_form,
            }
            )
