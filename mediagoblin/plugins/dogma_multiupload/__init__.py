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


from mediagoblin.tools import pluginapi
import os

PLUGIN_DIR = os.path.dirname(__file__)

def setup_plugin():
    
    # Link the templates to their respective views
    routes = [
                ('mediagoblin.plugins.dogma_multiupload.multi_upload_form',
                 '/dogma_multiupload/multiup',
                 'mediagoblin.plugins.dogma_multiupload.views:multi_upload_form'),
             ]
    #Register the routes
    pluginapi.register_routes(routes)
    # Register the template path.
    pluginapi.register_template_path(os.path.join(PLUGIN_DIR, 'templates'))



hooks = {
    'setup': setup_plugin
    }
