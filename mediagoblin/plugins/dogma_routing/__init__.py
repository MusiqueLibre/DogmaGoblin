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
from mediagoblin.tools import pluginapi
import os

_log = logging.getLogger(__name__)

PLUGIN_DIR = os.path.dirname(__file__)

def setup_plugin():

    _log.info('Setting up Dogma extra routing...')

    routes = [
          ('mediagoblin.plugins.dogma_routing.dogma_media_home',
          '/dogma/u/<string:user>/m/<string:media>/',
          'mediagoblin.plugins.dogma_routing.views:dogma_media_home'),
       ]

    pluginapi.register_routes(routes)
    pluginapi.register_template_path(os.path.join(PLUGIN_DIR, 'templates'))
def add_to_user_home_context(context):
    context['foo'] = 'bar'
    return context


hooks = {
    'setup': setup_plugin,
    ("mediagoblin.user_pages.user_home",
             "mediagoblin/user_pages/user.html"): add_to_user_home_context
    }
