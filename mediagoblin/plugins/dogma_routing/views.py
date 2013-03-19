
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
import datetime

from mediagoblin import messages, mg_globals
from mediagoblin.db.models import (MediaEntry, MediaTag, Collection,
                                   CollectionItem, User)
from mediagoblin.tools.response import render_to_response, render_404, redirect
from mediagoblin.tools.translate import pass_to_ugettext as _
from mediagoblin.tools.pagination import Pagination
from mediagoblin.tools.collection import collection_tools
from mediagoblin.user_pages import forms as user_forms
from mediagoblin.user_pages.lib import send_comment_email

from mediagoblin.decorators import (uses_pagination, get_user_media_entry,
    get_media_entry_by_id,
    require_active_login, user_may_delete_media, user_may_alter_collection,
    get_user_collection, get_user_collection_item, active_user_from_url)

from werkzeug.contrib.atom import AtomFeed


_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)

MEDIA_COMMENTS_PER_PAGE = 50


@get_user_media_entry
@uses_pagination
def dogma_media_home(request, media, page, **kwargs):
    """
    'Homepage' of a MediaEntry()
    """
    collection_form = user_forms.MediaCollectForm(request.form)
    media_home_logged(request, collection_form)

    comment_id = request.matchdict.get('comment', None)
    if comment_id:
        pagination = Pagination(
            page, media.get_comments(
                mg_globals.app_config['comments_ascending']),
            MEDIA_COMMENTS_PER_PAGE,
            comment_id)
    else:
        pagination = Pagination(
            page, media.get_comments(
                mg_globals.app_config['comments_ascending']),
            MEDIA_COMMENTS_PER_PAGE)

    comments = pagination()

    comment_form = user_forms.MediaCommentForm(request.form)

    media_template_name = media.media_manager['display_template']

    return render_to_response(
        request,
        media_template_name,
        {'media': media,
         'comments': comments,
         'pagination': pagination,
         'collection_form': collection_form,
         'comment_form': comment_form,
         'app_config': mg_globals.app_config})

# Prevents an error for anonymous users because user in not difined
@require_active_login
def media_home_logged(request, collection_form):
    collection_form.collection.query = Collection.query.filter_by(
        creator = request.user.id).order_by(Collection.title)
    return collection_form 
