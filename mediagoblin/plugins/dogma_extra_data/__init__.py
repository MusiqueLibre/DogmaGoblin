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

    _log.info('Setting up Dogma extra data...')

    routes = [
       ('mediagoblin.plugins.dogma_extra_data.process_extra_data',
        '/dogma_extra_data/submit',
        'mediagoblin.plugins.dogma_extra_data.views:processExtraData',
       ),
       ('mediagoblin.plugins.dogma_extra_data.add_band',
        '/dogma_extra_data/add_band',
        'mediagoblin.plugins.dogma_extra_data.views:addBand',
       ),
       ('mediagoblin.plugins.dogma_extra_data.dashboard',
        '/dashboard',
        'mediagoblin.plugins.dogma_extra_data.views:dashboard',
       ),

       ]

    pluginapi.register_routes(routes)
    pluginapi.register_template_path(os.path.join(PLUGIN_DIR, 'templates'))

    pluginapi.register_template_hooks(
        {"extra_sideinfo": "dogma_extra_data/display_extra_data.html"})

hooks = {
    'setup': setup_plugin
    }
