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


import os
import logging

_log = logging.getLogger(__name__)

from datetime import datetime
import time

from werkzeug.exceptions import Forbidden
from werkzeug.utils import secure_filename

from mediagoblin import messages
from mediagoblin import mg_globals

from mediagoblin.edit import forms
from mediagoblin.plugins.dogma import forms as dogma_forms
from mediagoblin.plugins.dogma_lib.lib import (save_pic, list_as_string, save_member_specific_role, get_albums, may_edit_object,
        convert_to_list_of_dicts, save_member_if_new, store_keywords, SaveListRole)
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
from mediagoblin.plugins.dogma.models import (DogmaBandDB, BandMemberRelationship, DogmaComposerDB, DogmaMemberDB, DogmaAuthorDB, DogmaKeywordDataDB) 
from mediagoblin.db.models import (Collection)
from mediagoblin.messages import add_message, SUCCESS

import mimetypes

@require_active_login
def removeBand(request):

    #GET MEMBER
    band = DogmaBandDB.query.filter_by(
        id = request.matchdict['band_id']).first()
    if not may_edit_object(request, band, 'creator'):
        raise Forbidden("User may not edit this band")


    form = dogma_forms.RemoveBandForm(request.form)
    #The creation date of the date is turned into milliseconds so it can be used by template's calendar
    if request.method == 'POST' and form.validate():

        band.delete()


        add_message(request, SUCCESS, _('Band successfully removed !'))
        return redirect(request, "mediagoblin.plugins.dogma.dashboard")

    return render_to_response(
        request,
        'dogma/remove/remove_band.html',
        {
            'band' : band,
            'form' : form,
         })
